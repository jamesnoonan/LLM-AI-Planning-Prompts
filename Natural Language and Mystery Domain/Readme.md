# BlocksWorld Natural language / Mystery domain converter.

Currently only works in terminal.

For Natural Language, copy & paste the input into terminal and enter to get results. Type "stop" to end (or just kill the terminal)

For Mystery Domain, the program will ask you for what to replace `ontop`, `block`, and `on the table` with. Then it is the same with natural language

## Supported Input format:

      1        3      2
      2        1  table
      3    table  table

where the first column is blocks name, the second column is what the block in on top of initially (i.e. block 1 is initially ontop of block 3), the thrid column is the goal state (i.e. block 1's goal state is to be ontop of block 2).