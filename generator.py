import sys
import os
import json

from domain_generators import BlocksWorldGenerator, Navigation2DGenerator, Navigation3DGenerator

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
    output_filename = f'./prompt-out/{input_filename.split("/")[-1].split(".")[0]}.json'

# Read the json data from the input file
with open(input_filename, "r") as input_file:
    input_data = json.load(input_file)

if (not ("domain" in input_data and "representation" in input_data and "nshot" in input_data, "data" in input_data)):
    print("Input file has an invalid format")
    sys.exit()    

# Check the problem domain to handle
domain = input_data.get("domain", "blocksworld")
match domain:
    case "blocksworld":
         generator = BlocksWorldGenerator(input_data)
    case "navigation-2d":
         generator = Navigation2DGenerator(input_data)
    case "navigation-3d":
         generator = Navigation3DGenerator(input_data)
    case _:
        print("Invalid domain in input file\n")
        sys.exit()


# Write the produced prompts to file
output_data = generator.prompts()

os.makedirs(os.path.dirname(output_filename), exist_ok=True)
with open(output_filename, "w") as output_file:
    output_file.write(json.dumps({'prompts': output_data}, indent = 4))

