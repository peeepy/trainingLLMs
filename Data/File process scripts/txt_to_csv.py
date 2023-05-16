import csv

with open('test.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = []
thread_title = ""
text = ""
for line in lines:
    # If line starts with "Title: ", we save it as thread_title
    if line.startswith("Title: "):
        # We remove the prefix before saving title
        thread_title = line.replace("Title: ", "").strip()
    
    # Else, we append this as part of message under same title
    else:
        text += " " + line.strip()
        
        # Once a sentence is complete or length exceeds 200 chars,
        # we add it to our data list so each row has one full sentence only.
        if len(text) > 200 or (len(line)>4 and ('.' in line[-3:-1] or '?' in line[-3:-1] or '!' in line[-3:-1])):
            data.append([thread_title, text])
            text=""
            
# If any last message left incomplete without being added to list, we add it here.
if(len(text)):
    data.append([thread_title, text])

with open('output.csv', mode='a', newline='') as outfile:
    writer = csv.writer(outfile)

    # Writing header row with column names "thread_title" and "text"
    writer.writerow(['thread_title', 'text'])

    # Writing each element of data to a new row in output CSV file
    for d in data:
        writer.writerow(d)