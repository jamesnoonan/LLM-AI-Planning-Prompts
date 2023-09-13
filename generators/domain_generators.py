import sys

class PromptGenerator:
    def __init__(self, input_data):
        self.domain = input_data.get("domain", "blocksworld")
        self.representation = input_data.get("representation", "nl-casual")
        self.nshot = input_data.get("nshot", 0)
        self.data = input_data.get("data", [])

    def prompts(self):
        prompt_list = []

        for case in self.data:
            current_prompt = f'{self.get_domain_text()}\n{self.get_problem_text(case)}\n{self.get_examples_text()}'
            prompt_list.append(current_prompt)

        return prompt_list

    def get_domain_text(self):
        return ""
    
    def get_problem_text(self, case):
        return ""
    
    def get_examples_text(self):
        output = ""

        for i in range(0, self.nshot):
            output += self.get_example_text(i)
        
        return output
    
    def get_example_text(self, index):
        return ""

class BlocksWorldGenerator(PromptGenerator):
    def get_domain_text(self):
        return "A set of wooden blocks of various shapes and colors are sitting on a table. The goal is to build one or more vertical stacks of blocks. Only one block may be moved at a time: it may either be placed on the table or placed atop another block. Because of this, any blocks that are, at a given time, under another block cannot be moved. Moreover, some kinds of blocks cannot have other blocks stacked on top of them."
    
    def get_problem_text(self, case):
        initial_text = ""
        goal_text = ""

        for stack in case.get("initial", []):
            initial_text += self.get_stack_text(stack)

        for stack in case.get("goal", []):
            goal_text += self.get_stack_text(stack)

        return f'The blocks are currently organised as follows: {initial_text}\nThe goal is to reorganise the blocks so that they look like: {goal_text}'
    
    def get_stack_text(self, stack):
        blocks = stack.split(',')
        stack_text = f'Block {blocks[0]} is on the table. '
        
        for i in range(1, len(blocks)):
            stack_text += f'Block {blocks[i]} is stacked on top of {blocks[i-1]}. '

        return stack_text

    
    def get_example_text(self, index):
        return ""

class Navigation2DGenerator(PromptGenerator):
    grid_domain_pddl_text = """
(define (domain grid-navigation)
(:requirements :strips :typing)

(:types
    cell
)

(:predicates
    (agent-at ?pos - cell)
    (obstacle-at ?pos - cell)  ; Obstacle-at predicate
    (neighbors ?pos1 - cell ?pos2 - cell)
)

(:action move
    :parameters (?from - cell ?to - cell)
    :precondition (and (agent-at ?from) (neighbors ?from ?to) (not (obstacle-at ?to))) 
    :effect (and (not (agent-at ?from)) (agent-at ?to))
)
)
"""
    def generate_problem_pddl(self, size, initial, goal, obstacles):
        width, height = map(int, size.split(","))
        init_x, init_y = map(int, initial.split(","))
        goal_x, goal_y = map(int, goal.split(","))
        
        # Generate objects
        objects = []
        for x in range(width):
            for y in range(height):
                objects.append(f"cell-{x}-{y}")
        objects_str = " ".join(objects)
        
        # Generate init states
        init_states = []
        init_states.append(f"(agent-at cell-{init_x}-{init_y})")
        
        # Generate neighbors
        for x in range(width):
            for y in range(height):
                if x + 1 < width:
                    init_states.append(f"(neighbors cell-{x}-{y} cell-{x+1}-{y})")
                    init_states.append(f"(neighbors cell-{x+1}-{y} cell-{x}-{y})") # ensure the reverse also holds
                if y + 1 < height:
                    init_states.append(f"(neighbors cell-{x}-{y} cell-{x}-{y+1})")
                    init_states.append(f"(neighbors cell-{x}-{y+1} cell-{x}-{y})")
        
        # Generate obstacles
        for obstacle in obstacles:
            obs_x, obs_y = map(int, obstacle.split(","))
            init_states.append(f"(obstacle-at cell-{obs_x}-{obs_y})")  
        
        init_states_str = "\n    ".join(init_states)
        
        # Generate the full PDDL string
        problem_pddl = f"""(define (problem grid-problem)
(:domain grid-navigation)
(:objects
    {objects_str}
)
(:init
    {init_states_str}
)
(:goal (agent-at cell-{goal_x}-{goal_y}))
)"""
    
        return problem_pddl
    

    def get_domain_text(self):
        match self.representation:
            case "nl-casual":
                return "You are a robot in a discrete finite grid. You start at a certain position and aim to reach the goal position. However, you can only move one square at a time and you cannot move diagonally. There may be obstacles in your path, which you cannot move onto or over. Coordinates are represented as (x,y)."
            case "nl-math":
                return "Let r denote a discrete, non-negative 2-dimensional point. The value of r is initially set to value s. A transition t is a list of two points where the distance between them is exactly one. Transitions cannot include a point that is in list o."
            case "pddl":
                return "You are currently solving the below planning problem represented by two files: a domain.pddl and a problem.pddl. \ Below is the domain.pddl file: \n" + self.grid_domain_pddl_text + "\\"

        return ""
    
    def get_problem_text(self, case):
        grid_size = case.get("size", "2,2").split(',')
        initial_pos = case.get("initial", "0,0")
        goal_pos = case.get("goal", "1,1")
        obstacles = case.get("obstacles", [])

        match self.representation:
            case "nl-casual":
                return f'The grid is {grid_size[0]} wide and {grid_size[1]} tall. You are initially located at ({initial_pos}) and you need to get to ({goal_pos}). {self.get_obstacles(obstacles)}\n Please reply only with the sequence of coordinates that you visit.'
            case "nl-math":
                return f'r may move no further than {int(grid_size[0]) - 1} on the x-axis and {int(grid_size[1]) - 1} on the y-axis. Let o={self.get_obstacles(obstacles)}. Given s=({initial_pos}) and g=({goal_pos}), what is the sequence of valid transitions needed to move r to g? Please reply only with this sequence.'
            case "pddl":
                return self.generate_problem_pddl(grid_size, initial_pos, goal_pos, obstacles)

        return ""

    def get_obstacles(self, obstacles):
        if (len(obstacles) == 0):
            match self.representation:
                case "nl-casual":
                    return "There are no obstacles."
                case "nl-math":
                    return "[]"
        elif (len(obstacles) == 1):
            match self.representation:
                case "nl-casual":
                    return f'There is an obstacle at ({obstacles[0]}).'
                case "nl-math":
                    return f'[{obstacles[0]}]'
        
        match self.representation:
            case "nl-casual":
                output = 'There are obstacles at '
                for i in range(0, len(obstacles) - 1):
                    output += f'({obstacles[i]}), '
                output += f'and ({obstacles[-1]}).'
            case "nl-math":
                output = '['
                for i in range(len(obstacles)):
                    output += f'({obstacles[i]}), '
                output += ']'


        return output
    
    def get_example_text(self, index):
        return ""

class Navigation3DGenerator(PromptGenerator):
    def get_domain_text(self):
        return ""
    
    def get_problem_text(self, case):
        return ""

    
    def get_example_text(self, index):
        return ""
