import csv

with open('prompt_generated.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = []
instruction = ""
input_text = ""
output_text = ""

# Loop through the lines in the input file and extract data based on keyword prefixes
for line in lines:
    if line.startswith("instruction:"):
        # If we have found a new instruction, save the previous one (if any) to our data list
        if instruction != "":
            data.append([instruction, input_text, output_text])

        # Update current instruction and reset input/output text fields
        instruction = line.replace("instruction:", "").strip()
        input_text = ""
        output_text = ""

    elif line.startswith("input:"):
        # Append any additional input content to our existing input text field
        input_text += " " + line.replace("input:", "").strip()

    elif line.startswith("output:"):
        # Append any additional output content to our existing output text field
        output_text += " " + line.replace("output:", "").strip()

# Save last row of data when end of file is reached (if a valid one exists)
if instruction != "":
    data.append([instruction, input_text, output_text])

# Write processed data to CSV

with open('output.csv', mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)

    # Writing header row with column names "instruction", "input", and "output"
    writer.writerow(['instruction', 'input', 'output'])

    # Writing each element of data to a new row in output CSV file
    for d in data:
        writer.writerow(d)