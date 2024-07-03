import json
import csv
from preprocess import preprocess_text

# Function to write comments to a CSV file
def write_comments_to_csv(subreddit, comments):
    csv_file = f'{subreddit}_comments.csv'
    header = ["subreddit", "comment"]

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(header)

        # Write the data rows
        for comment in comments:
            writer.writerow([subreddit, comment])

    print(f"CSV file '{csv_file}' created successfully.")

# Define variables for each subreddit
ask_a_liberal_comments = []
ask_a_conservative_comments = []
social_democracy_comments = []
the_donald_comments = []

# Define lists to store the body_cleaned for each subreddit
ask_a_liberal_body = []
ask_a_conservative_body = []
social_democracy_body = []
the_donald_body = []

# Map subreddit names to the corresponding variables
subreddit_mapping = {
    'AskALiberal': ask_a_liberal_comments,
    'askaconservative': ask_a_conservative_comments,
    'SocialDemocracy': social_democracy_comments,
    'The_Donald': the_donald_comments
}

# Open the JSON file
with open('comments_2019-01.json', 'r') as f:
    for i, line in enumerate(f):
        try:
            json_object = json.loads(line)
            subreddit = json_object.get('subreddit')
            if subreddit in subreddit_mapping:
                subreddit_mapping[subreddit].append(json_object)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e.msg}")

# Create a mapping for body_cleaned lists
body_mapping = {
    'AskALiberal': ask_a_liberal_body,
    'askaconservative': ask_a_conservative_body,
    'SocialDemocracy': social_democracy_body,
    'The_Donald': the_donald_body
}

# Extract 'body_cleaned' from each comment and append to the corresponding list
for subreddit, comments in subreddit_mapping.items():
    for comment in comments:
        body_cleaned = comment.get('body_cleaned')
        if body_cleaned is None:
            body_cleaned = ''  # Replace None with an empty string
        body_mapping[subreddit].append(preprocess_text(body_cleaned))

# Write each subreddit's comments to its own CSV file
write_comments_to_csv('AskALiberal', ask_a_liberal_body)
write_comments_to_csv('askaconservative', ask_a_conservative_body)
write_comments_to_csv('SocialDemocracy', social_democracy_body)
write_comments_to_csv('The_Donald', the_donald_body)







