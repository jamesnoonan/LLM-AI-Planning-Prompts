import os
import shutil
import datetime
import json

from prompt_generator import generate_prompts
from report_generator import generate_report
from response_generator import generate_responses

import llm

# Create temporary directory to store intermediate files
temp_folder = "/tmp_results"
os.makedirs(os.path.dirname(temp_folder), exist_ok=True)

#
# Generate test cases
#

with open("./examples/navigation2d-1.json", "r") as input_file:
    cases = json.load(input_file)


#
# Generate prompts
#
prompts = generate_prompts(cases, temp_folder + "/prompts.json")

#
# Run LLM to get results
#
model = llm.OpenAILLM()
responses = generate_responses(prompts, model, temp_folder + "/responses.json")

#
# Visualise cases and create report
#
domain = cases.get("domain", "none")
date_text = datetime.date.today().strftime("%Y-%m-%d")
time_text = datetime.datetime.now().time().strftime("%H-%M-%S")

output_filename = f'report-out/report-{domain}-{date_text}-{time_text}.md'
generate_report(cases, prompts, responses, output_filename)

# Clean up and delete the temp folder
shutil.rmtree(temp_folder)
