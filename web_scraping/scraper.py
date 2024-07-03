import csv
from utils import html_parser, get_speech_url, get_next_page_url, get_speech_words

class SpeechScraper:
    def __init__(self, base_url, country, speaker, class_name_url, prefix, tag_name_speech_words, class_name_speech_words):
        self.base_url = base_url
        self.country = country
        self.speaker = speaker
        self.class_name_url = class_name_url
        self.prefix = prefix
        self.tag_name_speech_words = tag_name_speech_words
        self.class_name_speech_words = class_name_speech_words
    def get_speeches(self, num_of_speeches):
        """
        Get words from a specified number of speeches.

        Args:
            num_of_speeches (int): The number of speeches to fetch.

        Returns:
            list: A list containing all the words found in the speeches.
        """
        list_speech_words = []
        collected_speeches = 0

        base_url = self.base_url
        class_name_url = self.class_name_url
        tag_name_speech_words = self.tag_name_speech_words
        class_name_speech_words = self.class_name_speech_words

        while collected_speeches < num_of_speeches:
            speech_urls = get_speech_url(base_url, class_name_url, self.prefix)
            for speech_url in speech_urls:
                if collected_speeches >= num_of_speeches:
                    break
                speech_words = get_speech_words([speech_url], tag_name_speech_words, class_name_speech_words)
                if not speech_words:  # Check if speech_words is empty
                    continue  # Skip this iteration if speech_words is empty
                list_speech_words.append(speech_words[0])
                collected_speeches += 1

            if collected_speeches < num_of_speeches:
                base_url = get_next_page_url(base_url)
        return list_speech_words

    def save_to_csv(self, speeches, filename):
        """
        Save the speeches to a CSV file.

        Args:
            speeches (list): The list of speeches.
            filename (str): The name of the CSV file to save.
        """
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Country', 'Number of Speeches', 'Speaker', 'Speech Content'])

            for speech in speeches:
                writer.writerow([self.country, len(speeches), self.speaker, speech])

        print(f"Data saved to {filename}")

    def process_speeches(url, country, speaker, class_name_url, prefix, tag_name_speech_words,
                         class_name_speech_words, num_of_speeches, filename):
        """
        Process speeches for a given set of parameters.

        Args:
            url (str): The URL to start scraping from.
            country (str): The country of the speaker.
            speaker (str): The name of the speaker.
            tag_name_speech_url (str): The tag name for speech URLs.
            class_name_url (str): The class name for speech URLs.
            prefix (str): The prefix for constructing full URLs.
            tag_name_speech_words (str): The tag name for speech content.
            class_name_speech_words (str): The class name for speech content.
            num_of_speeches (int): The number of speeches to scrape.
            filename (str): The name of the CSV file to save speeches to.
        """
        scraper = SpeechScraper(url, country, speaker, class_name_url, prefix,
                                tag_name_speech_words, class_name_speech_words)
        speeches = scraper.get_speeches(num_of_speeches)
        scraper.save_to_csv(speeches, filename)

