import os
import datetime
import re;

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

# Returns None if unable to parse
def parse_solution_string(response):
    try:
        coords = re.split(r'\s*->\s*', response)  # Split on arrows with optional spaces
        return [list(map(int, coord.strip("()").split(","))) for coord in coords]
    except:
        return None

# Checks if solution is from the initial state to the goal state, with each move
# only a single non-diagonal jump and no obstacles crossed
def is_valid_solution(path, obstacles, initial, goal):
    # Response must start at initial and finish at goal
    if path[0] != initial or path[-1] != goal:
        return False

    for i in range(len(path)):
        # Check if the cell is an obstacle
        if path[i] in obstacles:
            return False
        
        # Check for valid moves between consecutive cells
        if i > 0:
            dx = abs(path[i][0] - path[i-1][0])
            dy = abs(path[i][1] - path[i-1][1])
            
            # If the move is diagonal or jumps over blocks
            if dx + dy != 1:
                return False
            
    return True

# Note: this currently only is written for navigation 2D
def generate_result_md(folder, index, case, prompt, response):
    date_text = datetime.date.today().strftime("%Y-%m-%d")
    time_text = datetime.datetime.now().time().strftime("%H-%M-%S")
    image_filename = f'{date_text}-{time_text}-case{index}.png'

    cells = convert_string_to_tuple(case.get("size", "5,5"))
    initial_pos = convert_string_to_tuple(case.get("initial", "0,0"))
    goal_pos = convert_string_to_tuple(case.get("goal", "1,1"))
    obstacles = list(map(convert_string_to_tuple, case.get("obstacles", [])))
    path = parse_solution_string(response)

    if path == None:
        path_validity = "Syntax Error"
    else:
        path_validity = "Valid" if is_valid_solution(path, obstacles, initial_pos, goal_pos) else "Invalid"
    

    generate_image(cells, initial_pos, goal_pos, obstacles, path, f'{folder}/images/{image_filename}')

    return f"""## Test Case {index+1} [{path_validity}]

### Prompt

{prompt}
    
![Navigation task visualisation](./images/{image_filename})

### Response

{response}
"""

