"""
rss-search.py: an rss feed filter
"""
from feedparser import parse
from operator import or_
from urllib import urlretrieve
from os import mkdir
from time import strftime, localtime
from re import search

def get_list_from_string(s):
    """ returns a list of lines """
    return s.strip().split('\n')

def get_text_from_feed_entry(entry):
    """ returns a dict from entry containing text and link """
    return {'text': entry.title + '\n' + entry.summary, 'link': entry.link}
    
def matches_word(text, word):
    """ checks if text matches word """
    return search(r'\b'+word.lower()+r'\b', text.lower())


def matches_any_word(text, keywords):
    """ checks if text matches any of the keywords """
    return reduce(or_, [matches_word(text, word) for word in keywords])
    

def main(urls, keywords):
    """ main function """
    raw_data_list = [parse(url) for url in urls]
    entries = sum([raw_data.entries for raw_data in raw_data_list], [])

    required_data =  [get_text_from_feed_entry(entry) for entry in entries]

    print len(required_data)

    results = filter(
                lambda data: matches_any_word(data['text'], keywords), 
                required_data
              )

    if results:

        dirname = strftime('%d-%m-%y', localtime())
        mkdir(dirname)

        for i, result in enumerate(results):
            filename = dirname + '/' + str(i)+'.html'
            urlretrieve(result['link'], filename )

    else:
        print 'no results found.\n try again with more keywords and urls'
        
        

        
if __name__ == '__main__':
    with open('urls.txt') as f:
        URLS = get_list_from_string(f.read())

    with open('keywords.txt') as f:
        KEY_WORDS = get_list_from_string(f.read())
