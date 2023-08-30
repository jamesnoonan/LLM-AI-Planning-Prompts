# AI Planning LLM Prompts
A small tool to assist the generation of consistently formatted prompts for Large Language Models to test their task and motion planning capabilities.

## Prompt Generation
### Usage
It can be run using command line arguments (`python generator.py ./examples/blocksworld-1.json`) or interactively (`python generator.py`). When using command line arguments, the program takes up to arguments: the input file and output file (the output file can be omitted and it will be saved to `prompt-out` with the same filename as the input).

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


 
### Input Format
Data is read using the JSON format. Use the `domain`, `representation` and `nshot` properties to control how the data is handled. The `data` property stores a list of the cases to construct the prompts from. The format of the `data` property may be different for different domains.
```
{
    "domain": "blocksworld",
    "representation": "nl-casual",
    "nshot": 0,
    "data": [
        {
            "initial": ["a", "b", "c", "d"],
            "goal": ["a,b,c,d"]
        },
        {
            "initial": ["b", "a,c"],
            "goal": ["a,b,c"]
        },
        {
            "initial": ["a,b,c", "d"],
            "goal": ["a,b,c,d"]
        }
    ]
}
```

## Running Prompts on the LLM
The generated prompts can be run programmatically on OpenAI's models through the `run_llm.py` file.

### Setup
To run this, you will need an OpenAI account with API access. Once you have this, create an `.env` file in this directory with the following key value pairs:

```
OPENAI_ORG=<organisation-id-here>
OPENAI_API_KEY=<api-secret-key-here>
```

### Usage
It can be run using command line arguments (`python run_llm.py ./examples/blocksworld-1.json`) or interactively (`python run_llm.py`). When using command line arguments, the program takes up to arguments: the input file and output file (the output file can be omitted and it will be saved to `llm-out` with the same filename as the input).

### Models
Currently all the requests use the model `gpt-3.5-turbo-0613`, however in the future we will support a larger variety of models.