import json

with open('prompt.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(lines)
data = []
prompt = {}
for line in lines:
    if line.strip() == '':  # empty line indicates end of prompt
        if prompt:  # add completed prompt to data
            data.append(prompt)
            prompt = {}
    elif 'instruction' not in prompt:  # first non-empty line is instruction
        prompt['instruction'] = line.strip().replace('instruction:', '')
    elif 'input' not in prompt:  # second non-empty line is input
        prompt['input'] = line.strip().replace('input:', '')
    else:  # remaining non-empty lines are output
        prompt['output'] = prompt.get('output', '') + line.replace('output:', '')
    
if prompt:  # add final prompt to data
    data.append(prompt)

with open('output.json', 'w') as f:
    json.dump(data, f, indent=4)