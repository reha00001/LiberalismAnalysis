pip install mistral_inference


import requests
import pandas as pd
import os
import re
import json

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": "Bearer hf_*******************"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

folder_path = '/content/raw_speeches'

def read_column_from_csv(file_path, column_name):
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Check if the specified column exists in the CSV
    if column_name in data.columns:
        return data[column_name]
    else:
        print(f"Column '{column_name}' not found in {file_path}.")
        return None

column_name = 'Speech Content'  # Replace with the name of the column you want to extract

# Create a dictionary to store the columns from each CSV file
speech_data = {}

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        column_data = read_column_from_csv(file_path, column_name)

        if column_data is not None:
            speech_data[filename] = column_data

# Combine all texts into one long text per country
combined_speech_data = {}

for key, value in speech_data.items():
  combined_speech_data[key] = ' '.join(value)

# Process every 'size' words and pass it to LLM
def process_every_n_words(text, size):
  words = text.split()
  task = "For the text below, first produce a score on the scale of 0-10 on the relvance to liberalism, and then produce a liberalism score on the scale of 0-10 (10=most liberal, 0=most illiberal) with our definition of liberalism. The output should be a Python dictionary in the form of {'relevance_score':_, 'liberalism_score':_}"
  res = []
  counter = 0
  liberal_def = " Our definition of liberal language is one of political liberalism and is explicitly not referring to economic liberalism. Political liberalism is committed to individual freedoms and rights and is not wedded to any specific economic model. More concretely, we understand a public speech which promotes civil rights, gender equality, and pluralism as liberal, whereas we categorize as an illiberal speaker a head of government who bolsters nationalistic values and overemphasizes traditional structures and religion"

  for i in range(0, len(words)-size, size):
    if counter >= 170:
      return res
    chunk = words[i:i+size]
    input_text = ' '.join(chunk)
    try:
      output = query({
      "inputs": f"""Task: {task}\nDefinition: {liberal_def}\nText: {input_text}\nScore:""",
      'parameters': {'temperature': 0.01},
      'options': {'use_cache': False}
      })

      if not output:
        print('no output')

      try:
        cur_res = output[0]['generated_text']

        regex_res = re.search(r"Score:\s*(\{.*?\})", cur_res)
        if not regex_res:
          continue
        score_dict_str = regex_res.group(1)
        res.append(score_dict_str)
        counter += 1
      except KeyError as e:
        print('keyerror 1')
        break
    except KeyError as e:
      print('keyerror 2')

  return res

# Example Usage
list_turkey = process_every_n_words(combined_speech_data['tr_speeches.csv'], 50)

json_turkey = json.dumps(list_turkey)
with open('turkey_data.json', 'w') as f:
    json.dump(list_turkey, f)

