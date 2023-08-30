import os
import sys
import openai
import json
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

input_filename = None
output_filename = None

# Get input and output files
if (len(sys.argv) > 1):
    input_filename = sys.argv[1]
    if (len(sys.argv) > 2):
        output_filename = sys.argv[2]
else:
    input_filename = input('Input File (JSON): ')
    output_filename = input('Output File (JSON) [optional]: ')

if (not bool(input_filename)):
    sys.exit()
if (not bool(output_filename)):
    output_filename = f'./llm-out/{input_filename.split("/")[-1].split(".")[0]}.json'

# Read the json data from the input file
with open(input_filename, "r") as input_file:
    input_data = json.load(input_file)

if (not ("prompts" in input_data)):
    print("Input file has an invalid format")
    sys.exit()    

# Write the produced prompts to file
prompts = input_data.get("prompts", [])
output_data = []

tokens_used = 0

# Submit each prompt to the llm and save response
for i in range(len(prompts)):
    print(f'--- Generating {i+1} of {len(prompts)} ---')
    prompt = prompts[i]

    raw_response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=[{"role":"user", "content": prompt}])

    response = raw_response['choices'][0]['message']['content']
    tokens_used += raw_response['usage']['total_tokens']

    output_data.append({'prompt': prompt, 'response': response})

print(f'\n======\nTokens Used: {tokens_used}\n======\n')

os.makedirs(os.path.dirname(output_filename), exist_ok=True)
with open(output_filename, "w") as output_file:
    output_file.write(json.dumps({'results': output_data}, indent = 4))

