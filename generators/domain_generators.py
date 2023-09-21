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
    x y
  )

  (:predicates
    (succ-x ?a - x ?b - x)
    (succ-y ?a - y ?b - y)
    (robot-x ?x - x)
    (robot-y ?y - y)
    (obstacle ?x - x ?y - y)
  )

  (:action move-x
    :parameters (?from-x - x ?from-y - y ?to-x - x)
    :precondition (and (or (succ-x ?from-x ?to-x) (succ-x ?to-x ?from-x)) (robot-x ?from-x) (robot-y ?from-y) (not (obstacle ?to-x ?from-y)))
    :effect (and (not (robot-x ?from-x)) (robot-x ?to-x))
  )

  (:action move-y
    :parameters (?from-x - x ?from-y - y ?to-y - y)
    :precondition (and (or (succ-y ?from-y ?to-y) (succ-y ?to-y ?from-y)) (robot-x ?from-x) (robot-y ?from-y) (not (obstacle ?from-x ?to-y)))
    :effect (and (not (robot-y ?from-y)) (robot-y ?to-y))
  )
)
"""
    def generate_problem_pddl(self, size, initial, goal, obstacles):
        # Read instance stats
        width, height = map(int, size)
        init_x, init_y = map(int, initial.split(","))
        goal_x, goal_y = map(int, goal.split(","))
        
        # Generate objects
        x_objects = [f"x{i} - x" for i in range(width)]
        y_objects = [f"y{i} - y" for i in range(height)]
        
        objects_str = "\n    ".join(x_objects + y_objects)
        
        # Generate init states predicates
        init_states = []
        init_states.append(f"(robot-x x{init_x})")
        init_states.append(f"(robot-y y{init_y})")
        
        # Generate successor states predicates for x and y
        for i in range(width - 1):
            init_states.append(f"(succ-x x{i} x{i+1})")
        for i in range(height - 1):
            init_states.append(f"(succ-y y{i} y{i+1})")
        
        # Generate obstacles predicates
        for obstacle in obstacles:
            obs_x, obs_y = map(int, obstacle.split(","))
            init_states.append(f"(obstacle x{obs_x} y{obs_y})")
        
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
(:goal (and (robot-x x{goal_x}) (robot-y y{goal_y})))
)"""
        
        return problem_pddl
    
    def generate_problem_motion(self, size, initial, goal, obstacles):
        # Read instance stats
        width, height = map(int, size)
        init_x, init_y = map(int, initial.split(","))
        goal_x, goal_y = map(int, goal.split(","))

        def to_coord(x, y):
            # function that transfer grid-space representation to coordinate space representation
            return f'({x}, {y})'
        
        # Generate obstacles coordinates
        obs_centers = []
        for i in range(len(obstacles)):
            obs_x, obs_y = map(int, obstacles[i].split(","))
            obs_centers.append(f'o{i}-{to_coord(obs_x, obs_y)}')
        obs_centers_str = "; ".join(obs_centers)

        motion_string = f"""The rectangular-shaped space is defined from 0 to {width} on x-axis and 0 to {height} on y-axis. 
There is a square-shaped robot of side-length 1 whose intial left-lower corner position is located at {to_coord(init_x, init_y)}.
There are also {len(obs_centers)} square-shaped obstacles of side-length 1, their left-lower corner position is given below: 
{obs_centers_str}

The robot's movement must follow the following rules:
1) within each move, the robot can only move horizontally or vertically as a straight line, we do not restrict the distance to move in each movement
2) during the entire moving process, the entire robot square cannot go beyond the the space's boundary at any point, however we do allow the side of the robot to overlap with boundary
3) during the entire moving process, the entire robot square cannot overlap with any of the obstacle square at any point, not even partially. however we do allow their boundary to overlap

Based on the above rule, we will be able to consider the left-lower corner positions of robot before/after each move as vertices, and the movement as a straght line edge.
Thus, we define a movement of robot center from (x1,y1) to (x2, y2) as "edge[(x1, y1) -> (x2, y2)]"
Please notice that Not just the vertices (robot's position before and after each move) but also the entire path between any two vertices must not overlap with the obstacles.

The goal is to find an optimal path composed by many valid movements that transfer the robot's left-lower corner position to {to_coord(goal_x,goal_y)}
Please solve the above question as a simple motion-planning problem. Your solution of optimal path should contain total n movement in the format of 
"(x0, y0)->(x1, y1)->...->(xn, yn)" 
where (x0, y0) is the initial square robot's left-lower corner coordinate and (xn, yn) should the goal left-lower corner coordinate of the robot after n valid movement. Meanwhile each -> represent one movement.
"""
        return motion_string

    def get_domain_text(self):
        match self.representation:
            case "nl-casual":
                return "You are a robot in a discrete finite grid. You start at a certain position and aim to reach the goal position. However, you can only move one square at a time and you cannot move diagonally. There may be obstacles in your path, which you cannot move onto or over. Coordinates are represented as (x,y)."
            case "nl-math":
                return "Let r denote a discrete, non-negative 2-dimensional point. The value of r is initially set to value s. A transition t is a list of two points where the distance between them is exactly one. Transitions cannot include a point that is in list o."
            case "motion":
                return "Consider a simple 2-dimensional motion planning navigation problem. \n The problem happenes on a 2-d rectangular-shaped space where each point within the space can be represented by two real-number coordinates in x-axis and y-axis as (x,y). \n "
            case "pddl":
                return "Please solve the 2-dimensional grid-space-based navigation problem represented in Planning Domain Definition Language (PDDL), the problem is definded under two files: a domain.pddl which defines the domain environment of problem, and a problem.pddl which describe the problem instance. \n Below is the domain.pddl file in text: \n" + self.grid_domain_pddl_text + "\n"

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
            case "motion":
                return f'{self.generate_problem_motion(grid_size, initial_pos, goal_pos, obstacles)}. \n Please reply only with the sequence of coordinates connected by -> in the optiaml path and nothing else, not even explanation text.'
            case "pddl":
                return f"""Below is the problem.pddl file in text: \n {self.generate_problem_pddl(grid_size, initial_pos, goal_pos, obstacles)} \n Your optimal plan should containing a sequence of actions of move-x and move-y that lead the robot to the goal. 
Meanwhile there will be a sequence of change in "robot-x xi" and "robot-y yj" as the effect of each move on robot's position, every position can be transformed into a coordinate (i, j) where both i and j are integer value. So the final path can be transformed into a sequence of coordinates. 
Please solve the problem and output using the following format with no other explanation: 
""(i_0,j_0)->(i_1,j_1)...->(i_n,j_n)"" 
where each (i_a, j_a) correpond to the coordinate of robots after ath movement of the optimal path, i_a,j_a should both be integer value dervied from robot-x xi_a and robot-y yj_a"""
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
        return "If you cannot find a valid solution, please return only '(-1, -1)' if no optimal path found and nothing else."

class Navigation3DGenerator(PromptGenerator):
    def get_domain_text(self):
        return ""
    
    def get_problem_text(self, case):
        return ""

    
    def get_example_text(self, index):
        return ""
