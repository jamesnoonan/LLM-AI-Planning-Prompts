import os
import datetime

from visualization import generate_image

def generate_report(cases, prompts, responses, output_filename):
    folder = '/'.join(output_filename.split('/')[:-1])
    # Create folders if needed
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Generate Markdown
    output_data = generate_title_md(cases)

    cases_data = cases.get('data', [])
    prompts_data = prompts.get('prompts', [])
    responses_data = responses.get('results', [])

    if (cases.get('domain', 'none') == 'navigation-2d'):
        for i in range(len(cases_data)):
            output_data += generate_result_md(folder, i, cases_data[i], prompts_data[i], responses_data[i].get("response", ""))

    # Save to file and return
    with open(output_filename, "w") as output_file:
        output_file.write(output_data)
    return output_data


def generate_title_md(cases):
    time_text = datetime.datetime.now().time().strftime("%H:%M:%S")
    date_text = datetime.date.today().strftime("%d/%m/%Y")

    return f"""# LLM Planning Report

> Generated at {time_text} on {date_text}

- **Domain**: {cases.get('domain', 'none')}
- **Representation**: {cases.get('representation', 'none')}
- **Examples Given to LLM**: {cases.get('nshot', 'none')} examples
- **Count**: {len(cases.get('data', []))} test cases

"""

def convert_string_to_tuple(input):
    values = input.split(",")
    return list(map(int, values))

# Note: this currently only is written for navigation 2D
def generate_result_md(folder, index, case, prompt, response):
    date_text = datetime.date.today().strftime("%Y-%m-%d")
    time_text = datetime.datetime.now().time().strftime("%H-%M-%S")
    image_filename = f'{date_text}-{time_text}-case{index}.png'

    cells = convert_string_to_tuple(case.get("size", "5,5"))
    initial_pos = convert_string_to_tuple(case.get("initial", "0,0"))
    goal_pos = convert_string_to_tuple(case.get("goal", "1,1"))
    obstacles = list(map(convert_string_to_tuple, case.get("obstacles", [])))

    generate_image(cells, initial_pos, goal_pos, obstacles, f'{folder}/images/{image_filename}')

    return f"""## Test Case {index+1}

### Prompt

{prompt}
    
![Navigation task visualisation](./images/{image_filename})

### Response

{response}

"""

