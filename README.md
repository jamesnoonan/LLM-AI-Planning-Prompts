# AI Planning LLM Prompts
A small tool to assist the generation of consistently formatted prompts for Large Language Models to test their task and motion planning capabilities.

## Prompt Generation
### Usage
The LLM tests can be run using command line arguments (`python main.py 5 3 3`) or interactively (`python main.py`). When using command line arguments, the program takes up to three arguments: the problem size, the number of cases to generate, and the number of obstacles to generate. Any arguments not given will be asked for using standard input.

The report will be written to the `report-out` folder in Markdown.

*Note: The generation is made up of multiple steps, which can be run individually if needed. The results will saved to a JSON file.*

### Domains
The `domain` property changes the type of problem. The currently supported domains are:
- Blocks world (`blocksworld`)
- 2D Navigation/Grid world (`navigation-2d`)
- 3D Navigation (`navigation-3d`) - *In progress*

### Representations
The `representation` property will change the structure and language of the prompts.
The currently supported representations are:
- Natural Language Casual (`nl-casual`)
- Natural Language Formal (`nl-formal`) - *In progress*
- PDDL (`pddl`)  - *In progress*
