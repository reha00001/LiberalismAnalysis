from scraper import SpeechScraper

def main():
    #Get UK speeches
    uk_url = 'https://www.gov.uk/search/news-and-communications?people%5B%5D=rishi-sunak&order=updated-newest'
    uk_num_of_speeches = 150
    uk_country = 'UK'
    uk_speaker = 'Rishi Sunak'
    uk_filename = 'uk_speeches.csv'
    uk_class_name_url = 'ul.gem-c-document-list.gem-c-document-list--no-underline'
    uk_prefix = 'https://www.gov.uk'
    uk_tag_name_speech_words = 'div'
    uk_class_name_speech_words = 'govspeak'

    SpeechScraper.process_speeches(uk_url, uk_country, uk_speaker, uk_class_name_url, uk_prefix, uk_tag_name_speech_words, uk_class_name_speech_words, uk_num_of_speeches, uk_filename)

    # Get Hungary speeches
    hu_url = 'https://abouthungary.hu/speeches-and-remarks?page=1'
    hu_num_of_speeches = 130
    hu_country = 'Hungary'
    hu_speaker = 'Viktor Orbán'
    hu_filename = 'hu_speeches.csv'
    hu_class_name_url = '.articles .container .row .col-12 .row'
    hu_prefix = 'https://abouthungary.hu/'
    hu_tag_name_speech_words = 'div'
    hu_class_name_speech_words = 'article__content'

    SpeechScraper.process_speeches(hu_url, hu_country, hu_speaker, hu_class_name_url, hu_prefix, hu_tag_name_speech_words, hu_class_name_speech_words, hu_num_of_speeches, hu_filename)

    # Get the Netherlands speeches
    nl_url = 'https://www.government.nl/documents?keyword=speech%20mark%20rutte&page=1'
    nl_num_of_speeches = 45
    nl_country = 'The Netherlands'
    nl_speaker = 'Mark Rutte'
    nl_filename = 'nl_speeches.csv'
    nl_class_name_url = 'ol.common.results'
    nl_prefix = 'https://www.government.nl'
    nl_tag_name_speech_words = 'div'
    nl_class_name_speech_words = 'article content'

    SpeechScraper.process_speeches(nl_url, nl_country, nl_speaker, nl_class_name_url, nl_prefix, nl_tag_name_speech_words, nl_class_name_speech_words, nl_num_of_speeches, nl_filename)



if __name__ == "__main__":
    main()


