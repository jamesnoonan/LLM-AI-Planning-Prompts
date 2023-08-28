continue_work = True

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
    output = f"There are {block_count} blocks. "
    
    for i in data:
        block_name = f"Block {i[0]}"
        
        if i[1] != "table":
            output += f"{block_name} is on top of Block {i[1]}, "
        else:
            output += f"{block_name} is on the table, "
    
    output = output[:-2] + ". The goal is to move "
    
    for i in data:
        block_name = f"Block {i[0]}"
        
        if i[2] != "table":
            output += f"{block_name} on top of Block {i[2]}, "
        else:
            output += f"{block_name} on the table, "
    
    output += "how to achieve this?"
    print(output)
