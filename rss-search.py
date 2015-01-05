"""
news.py: an rss feed aggregator/filter
"""
from feedparser import parse
from operator import or_
from urllib import urlretrieve
from os import mkdir, path
from time import strftime, localtime
from re import search

LIM = 3

def get_list_from_string(s):
    """ returns a list of lines """
    return s.strip().splitlines()

def get_text_from_feed_entry(entry):
    """ returns a dict from entry containing text and link """
    return {'text': entry.title + '\n' + entry.summary, 'link': entry.link}
    
def matches_word(text, word):
    """ checks if text matches word """
    if search(r'\b'+word.lower()+r'\b', text.lower()):
        return True
    else:
        return False


def matches_any_word(text, keywords):
    """ checks if text matches any of the keywords """
    return reduce(or_, [matches_word(text, word) for word in keywords])
    
def make_filename(text, words=LIM ,extension=None):
    """ forms filename from text """
    filename = '-'.join(text.split(' ')[:LIM])
    if extension:
        filename += extension
    return filename

def main(urls, keywords):
    """ main function """
    raw_data_list = [parse(url) for url in urls]
    entries = sum([raw_data.entries for raw_data in raw_data_list], [])

    required_data =  [get_text_from_feed_entry(entry) for entry in entries]
    
    print 'searching {} entries...'.format(len(required_data))
    results = filter(
                lambda data: matches_any_word(data['text'], keywords), 
                required_data
              )


    if results:

        dirname = strftime('%d-%m-%y', localtime())
        if not path.isdir(dirname):
            mkdir(dirname)
                    
        RESULT_COUNT = len(results)
        
        print '{} result(s) found'.format(RESULT_COUNT)
        
        for i, result in enumerate(results):
            filename = path.join(
                        dirname,
                        make_filename(result['text'], extension = '.html')
                       )
            print 'downloading {} of {}...'.format(i+1, RESULT_COUNT),
            urlretrieve(result['link'], filename )
            print 'done'

    else:
        print 'no results found.\n try again with more keywords and urls'
        
        

        
if __name__ == '__main__':
    with open('urls.txt') as f:
        URLS = get_list_from_string(f.read())

    with open('keywords.txt') as f:
        KEY_WORDS = get_list_from_string(f.read())
    
    main(URLS, KEY_WORDS)
