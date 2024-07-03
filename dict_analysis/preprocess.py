import pandas as pd
import re
import nltk
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK resources
nltk.download('stopwords')

# Initialize the stemmer and stopwords list
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    # Remove punctuation (P) and numbers (N)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers

    # Convert to lowercase (L)
    text = text.lower()

    # Apply stemming (S)
    text = ' '.join([stemmer.stem(word) for word in text.split()])

    # Remove stopwords (W)
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text


def load_and_preprocess_csvs(folder_name, output_folder):
    data_dir = Path.cwd() / folder_name
    output_dir = Path.cwd() / output_folder
    output_dir.mkdir(exist_ok=True)

    # Iterate over all CSV files in the directory
    for file_path in data_dir.glob('*.csv'):
        df = pd.read_csv(file_path)

        # Apply preprocessing to 'Speech Content' column
        df['Speech Content'] = df['Speech Content'].apply(preprocess_text)

        # Save the processed DataFrame to a new CSV file in the output directory
        output_file_path = output_dir / file_path.name
        df.to_csv(output_file_path, index=False)

        print(f"Preprocessed data saved to {output_file_path}")



