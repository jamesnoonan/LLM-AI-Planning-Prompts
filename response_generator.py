import os
import sys
import json
import llm

def generate_responses(input_data, model, output_filename):
    if (not ("prompts" in input_data)):
        print("Input file has an invalid format")
        sys.exit()    

    prompts = input_data.get("prompts", [])
    output_data = []

    tokens_used = 0

    # Submit each prompt to the llm and save response
    for i in range(len(prompts)):
        print(f'--- Generating {i+1} of {len(prompts)} ---')
        prompt = prompts[i]

        response = model.get_response(prompt)
        if model.has_tokens:
            tokens_used += model.get_tokens()

        output_data.append({'prompt': prompt, 'response': response})

    print(f'\n======\nTokens Used: {tokens_used}\n======\n')

    output_data = {'results': output_data}

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, "w") as output_file:
        output_file.write(json.dumps(output_data, indent = 4))

    return output_data


# If script is run directly, parse input and output files
if __name__ == "__main__":
    input_filename = None
    output_filename = None

    # Get llm object to get responses from
    if (len(sys.argv) > 1):
        if sys.argv[1] == "gpt":
            model = llm.OpenAILLM()
        elif sys.argv[1] == "bard":
            model = llm.BardLLM()
        else:
            print("Invalid LLM option")
            sys.exit()


        # Get input and output files
        if (len(sys.argv) > 2):
            input_filename = sys.argv[2]
            if (len(sys.argv) > 3):
                output_filename = sys.argv[3]
    else:
        model = llm.OpenAILLM()  # FIXME use LLM specified by user input
        input_filename = input('Input File (JSON): ')
        output_filename = input('Output File (JSON) [optional]: ')

    if (not bool(input_filename)):
        sys.exit()
    if (not bool(output_filename)):
        output_filename = f'./llm-out/{input_filename.split("/")[-1].split(".")[0]}.json'

    # Read the json data from the input file
    with open(input_filename, "r") as input_file:
        input_data = json.load(input_file)
        generate_responses(input_data, model, output_filename)
