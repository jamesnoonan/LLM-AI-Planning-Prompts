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
    def get_domain_text(self):
        match self.representation:
            case "nl-casual":
                return "You are a robot in a discrete finite grid. You start at a certain position and aim to reach the goal position. However, you can only move one square at a time and you cannot move diagonally. There may be obstacles in your path, which you cannot move onto or over. Coordinates are represented as (x,y)."
            case "nl-math":
                return "Let r denote a discrete, non-negative 2-dimensional point. The value of r is initially set to value s. A transition t is a list of two points where the distance between them is exactly one. Transitions cannot include a point that is in list o."


        return ""
    
    def get_problem_text(self, case):
        grid_size = case.get("size", "2,2").split(',')
        initial_pos = case.get("initial", "0,0")
        goal_pos = case.get("goal", "1,1")
        obstacles = case.get("obstacles", [])

        match self.representation:
            case "nl-casual":
                return f'The grid is {grid_size[0]} wide and {grid_size[1]} tall. You are initially located at ({initial_pos}) and you need to get to ({goal_pos}). {self.get_obstacles(obstacles)}\n Please reply only with the sequence of coordinates that you visit and no explanations. Use -> to connect the coordinates.'
            case "nl-math":
                return f'r may move no further than {int(grid_size[0]) - 1} on the x-axis and {int(grid_size[1]) - 1} on the y-axis. Let o={self.get_obstacles(obstacles)}. Given s=({initial_pos}) and g=({goal_pos}), what is the sequence of valid transitions needed to move r to g? Please reply only with this sequence and no explanations. Use -> to connect the coordinates.'
            
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
