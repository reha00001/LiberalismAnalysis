import requests
import csv
from bs4 import BeautifulSoup


def html_parser(url):
    """
    Parse HTML content from a given URL.

    Args:
        url (str): The URL of the webpage to parse.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML content.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    # connect to url
    page = requests.get(url, headers=headers)

    # parse the html
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_speech_url(url, class_name, prefix):
    """
    Extract speech URLs from a webpage.

    Args:
        url (str): The URL of the webpage to extract speech URLs from.
        class_name (str): The class name of the elements containing the URLs of the speeches.
        prefix (str): The prefix of the website; e.g., 'https://www.gov.uk'.

    Returns:
        list: A list of speech URLs extracted from the webpage, with duplicates removed.
    """
    soup = html_parser(url)

    # get all the speech urls in a given page
    page_elements = soup.select(class_name)
    speech_urls_set = set()  # use a set to avoid duplicates
    for page_element in page_elements:
        for a_tag in page_element.find_all('a', href=True):
            href = a_tag['href']
            full_url = prefix + href
            speech_urls_set.add(full_url)

    # Convert the set back to a list
    list_speech_urls = list(speech_urls_set)

    return list_speech_urls



def get_speech_words(list_speech_urls, tag_name, class_name):
    """
    Extract words from speeches.

    Args:
        list_speech_urls (list): A list of speech URLs from which to extract words.
        tag_name(str) : The tag name to the words
        class_name (str) : The class name to the words

    Returns:
        list: A list containing all the words found in the speeches.
    """
    list_speech_words = []  # contains all the words in a given speech
    for url in list_speech_urls:
        soup = html_parser(url)
        # get the literal words from the speech
        words_elements = soup.find(tag_name, class_=class_name)
        if words_elements is not None:
            words_text = words_elements.get_text(strip=True).replace('\xa0', ' ').replace('\n',' ')
            list_speech_words.append(words_text)

    return list_speech_words


from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def get_next_page_url(url):
    """
    Get the URL of the next page by incrementing the page number in the query string.

    Args:
        url (str): The URL of the current page.

    Returns:
        str: The URL of the next page with the page number incremented by 1.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Increment the page number
    if 'page' in query_params:
        query_params['page'] = [str(int(query_params['page'][0]) + 1)]
    else:
        query_params['page'] = ['2']  # If there's no page parameter, add it starting from page 2

    # Construct the new query string
    new_query_string = urlencode(query_params, doseq=True)

    # Construct the new URL
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query_string,
        parsed_url.fragment
    ))

    return new_url


def save_to_csv(country, speaker, speeches, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Number of Speeches', 'Speaker', 'Speech Content'])

        for speech in speeches:
            writer.writerow([country, len(speeches), speaker, speech])

    print(f"Data saved to {filename}")
