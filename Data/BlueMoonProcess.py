import pandas as pd
import nltk
import json

# Download the NLTK tokenizer model (you only need to do this once)
nltk.download('punkt')

# Define a custom function to concatenate the "message_username" and "message" columns
def concatenate_message(row):
    return f"{row['message_username']}: {row['message']}"

# Open the Parquet file using Pandas
df = pd.read_parquet('train-00000-of-00001-9276d1ce89875933.parquet')

def get_thread_messages(thread_title):
    # Group messages by thread_title
    grouped = df.groupby('thread_title')
    
    # Select the batch of messages with the specified thread_title
    batch = grouped.get_group(thread_title)
    concatenated_messages = batch.apply(concatenate_message, axis=1)
    
    # Store the first row name and second row name as variables
    first_row_name = batch.iloc[0]['message_username']
    second_row_name = batch.iloc[1]['message_username']
    end_name = f"{second_row_name}: "
    end_name_split = f"{second_row_name}: "
    print(f'end_name: {end_name}')
    print(f'end_name_split: {end_name_split}')

    # Split the concatenated messages into two lists
    list1 = ["<START>", concatenated_messages.iloc[0], end_name]
    list2 = []
    num = 0
    for i in range(1, len(batch), 3):
        if num == 0:
            list2.append(concatenated_messages.iloc[i].split(end_name_split)[1])
            num += 1
            
        # print(batch.iloc[i]['message_username'])
        list2.append(concatenated_messages.iloc[i])
    # Return the two lists as a dictionary
    return {"Input": list1, "Output": list2}


# Group messages by thread_title
grouped = df.groupby('thread_title')

# Loop through every thread title and get the messages
for thread_title in grouped.groups.keys():
    length_group = len(grouped.get_group(thread_title))
    if length_group > 3:
        result_dict = get_thread_messages(thread_title)

     
        input_json = '\n'.join(result_dict["Input"])
        print(f'input_json: {input_json}')
        output_json = '\n'.join(result_dict["Output"])
        print(f'output_json: {output_json}')

        # Write list1_string and list2_string to a JSON file
        # Define the dictionary
        data = {"input": input_json, "output": output_json}
        with open('output.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')