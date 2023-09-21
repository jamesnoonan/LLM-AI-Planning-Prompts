import os
import shutil
import datetime
import sys

# Import the generator scripts
sys.path.insert(0, './generators')
from generators import case_generator, prompt_generator, response_generator, report_generator, llm

# Modify this list to change which representations are run
representations = ["nl-casual", "nl-math", "pddl", "motion"]


size = None
count = None
obstacles = None

# If script is run directly, parse parameters
if __name__ == "__main__":
    # Get input and output files
    if (len(sys.argv) > 1):
        size = int(sys.argv[1])
        if (len(sys.argv) > 2):
            count = int(sys.argv[2])
            if (len(sys.argv) > 3):
                obstacles = int(sys.argv[3])
    

if (size == None):
    size = int(input("Problem Size [5]: ") or "5")
if (count == None):
    count = int(input("Number of Cases [3]: ") or "3")
if (obstacles == None):
    obstacles = int(input("Obstacle Count (-1 for random) [-1]: ") or "-1")

# Given test cases to solve, will run through llm and save to report
def solve_cases(cases):
    #
    # Generate prompts
    #
    prompts = prompt_generator.generate_prompts(cases, temp_folder + "/prompts.json")

    #
    # Run LLM to get results
    #
    model = llm.OpenAILLM()
    responses = response_generator.generate_responses(prompts, model, temp_folder + "/responses.json")

    #
    # Visualise cases and create report
    #
    # domain = cases.get("domain", "none")
    representation = cases.get("representation", "none")
    date_text = datetime.date.today().strftime("%Y-%m-%d")
    time_text = datetime.datetime.now().time().strftime("%H-%M-%S")

    output_filename = f'report-out/report-{date_text}-{time_text}-{representation}.md'
    report_generator.generate_report(cases, prompts, responses, output_filename)


# Create temporary directory to store intermediate files
temp_folder = "./tmp_results"
os.makedirs(os.path.dirname(temp_folder), exist_ok=True)

#
# Generate test cases
#
cases = case_generator.generate_cases(
    {
        "size": size,
        "count": count,
        "obstacles": obstacles,
    },
    "navigation-2d",
    "nl-casual",
    0,
    temp_folder + "/cases.json")

# Run same test cases for different representations
for representation in representations:
    print(f'|||\n||| Generating results for {representation}\n|||')
    cases_cpy = cases.copy()
    cases_cpy["representation"] = representation
    solve_cases(cases_cpy)


# Clean up and delete the temp folder
shutil.rmtree(temp_folder)
