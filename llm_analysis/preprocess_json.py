import json
import os
import re
import matplotlib.pyplot as plt


def calculate_weighted_averages(folder_name):
    # Initialize the result dictionary
    weighted_averages = {}

    # Regular expression pattern
    pattern = r"relevance_score': (\d{1,2}).*liberalism_score': (\d{1,2})"

    for file_name in os.listdir(folder_name):
        # Construct the full file path
        file_path = os.path.join(folder_name, file_name)

        # Check if the file is a JSON file
        if file_name.endswith('.json'):
            # Open the JSON file and load the data
            with open(file_path, 'r') as file:
                data = json.load(file)

            sum_weight = 0
            sum_weight_score = 0

            # Process each item in the JSON data
            for item in data:
                # Find matches
                match = re.search(pattern, item)
                if match:
                    weight = int(match.group(1))
                    score = int(match.group(2))
                    sum_weight += weight
                    sum_weight_score += (score * weight)

            # Calculate the weighted average
            if sum_weight != 0:
                weighted_avg = sum_weight_score / sum_weight
            else:
                weighted_avg = 0

            # Store the result in the dictionary
            weighted_averages[file_name[:-5]] = weighted_avg

    return weighted_averages


def process_folder(folder_name):
    result = calculate_weighted_averages(folder_name)

    # Sort the dictionary by values (weighted averages) in descending order
    sorted_results = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=False)}
    sorted_results = {k: [v] for k, v in sorted_results.items()}

    # Add details to the dict
    sorted_results['north_korea'].extend(['North Korea - Kim Jong Un', 'red'])
    sorted_results['russia'].extend(['Russia - Vladimir Putin', 'red'])
    sorted_results['hungary'].extend(['Hungary - Viktor Orbán', 'red'])
    sorted_results['kazakhstan_1'].extend(['Kazakhstan - Kassym-Jomart Tokayev', 'red'])
    sorted_results['indonesia'].extend(['Indonesia - Joko Widodo', 'green'])
    sorted_results['cameroon'].extend(['Cameroon - Paul Biya', 'red'])
    sorted_results['kazakhstan_2'].extend(['Kazakhstan - Nursultan Nazarbayev', 'red'])
    sorted_results['turkey'].extend(['Turkey - Recep Tayyip Erdogan', 'red'])
    sorted_results['united_kingdom'].extend(['UK - Rishi Sunak', 'green'])
    sorted_results['united_states'].extend(['United States of America - Joe Biden, Kamala Harris', 'green'])
    sorted_results['netherlands'].extend(['The Netherlands - Mark Rutte', 'green'])

    # Extract avgs, file names, and color
    value_list = list(sorted_results.values())
    weighted_avgs = [value[0] for value in value_list]
    file_names = [value[1] for value in value_list]
    colors = [value[2] for value in value_list]

    # Plotting
    plt.figure(figsize=(13, 6))
    plt.scatter(weighted_avgs, range(len(file_names)), color=colors, marker='o', s=100)
    plt.yticks(range(len(file_names)), file_names)  # Set y-axis ticks to display file names
    plt.xlabel('Weighted Average Score')
    plt.title('Liberalness Score Analysis using Hugging Face Mistral Model')
    plt.xlim(0, 10)  # Set x-axis limit from 0 to 10
    plt.grid(True)  # Enable grid
    plt.tight_layout()
    plt.annotate('Illiberal', xy=(0, -0.1), xycoords='axes fraction', ha='center', va='center', fontsize=12)
    plt.annotate('Liberal', xy=(0.975, -0.1), xycoords='axes fraction', ha='center', va='center', fontsize=12)
    plt.show()
