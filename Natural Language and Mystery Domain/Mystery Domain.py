continue_work = True

print("What to replace blocks?")
blocks_replace = input()

print("What to replace ontop?")
ontop_replace = input()

print("What to replace on the table?")
table_replace = input()

while continue_work:
    data = []
    line = input()
    
    while line:
        if line == "stop":
            continue_work = False
            break
        
        line = line.strip()
        tokens = line.split()
        data.append(tokens)
        line = input()
    
    if not continue_work:
        break
    
    block_count = len(data)
    output = f"There are {block_count} {blocks_replace}s. "
    
    for i in data:
        block_name = f"{blocks_replace} {i[0]}"
        
        if i[1] != "table":
            output += f"{block_name} is {ontop_replace} {blocks_replace} {i[1]}, "
        else:
            output += f"{block_name} is {table_replace}, "
    
    output = output[:-2] + ". The goal is to move "
    
    for i in data:
        block_name = f"{blocks_replace} {i[0]}"
        
        if i[2] != "table":
            output += f"{block_name} {ontop_replace} {blocks_replace} {i[2]}, "
        else:
            output += f"{block_name} {table_replace}, "
    
    output += "How to achieve this?"

    rules = f"\n\nYou may move a {blocks_replace} {table_replace} only if no {blocks_replace} is {ontop_replace} it, and move a source {blocks_replace} {ontop_replace} another target {blocks_replace} only if no {blocks_replace} is {ontop_replace} the source and target {blocks_replace}."
    
    output += rules
    print(output)
