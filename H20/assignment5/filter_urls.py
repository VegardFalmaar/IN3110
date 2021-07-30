import requests as req
import re
from requesting_urls import get_html

def find_urls(text, base_url='', output=None):
    """Return a list of all urls in a body of text.

    Args:
        text (str): html string in which to search for urls
        base_url (str, optional): 
            the base url to be combined with relative urls found in text
        output (str, optional): path to file to which the matches will be saved

    Returns:
        urls (list of str objects): all the urls found in text

    """
    # find relative urls starting with a single forward slash /
    rel_urls = re.compile(r"""
        <a.*?href="     # match <a and start to read from the " following href=
        ((?:/[^/:]+?)+) # match relative urls on the form /relative/url
        (?:\#.*?)?"     # read past without keeping anything following #
        .*?</a>         # match the end of the block""", re.VERBOSE)
    rel_matches = rel_urls.findall(text)
    rel_matches = list(set(rel_matches))    # remove duplicates
    rel_matches = [base_url[:-1] + rel_url for rel_url in rel_matches]

    # find relative urls starting with a double forward slash //
    rel2_urls = re.compile(r"""
        <a.*?href="     # match <a and start to read from the " following href=
        (/(?:/[^:]*?)+) # match relative urls on the form //relative/url
        (?:\#.*?)?"     # read past without keeping anything following #
        .*?</a>         # match the end of the block
        """, re.VERBOSE)
    rel2_matches = rel2_urls.findall(text)
    rel2_matches = list(set(rel2_matches))  # remove duplicates
    start = base_url.split('//')[0]
    rel2_matches = [start + rel2_url for rel2_url in rel2_matches]

    # match absolute urls
    abs_urls = re.compile(r"""
        <a.*?href="     # match <a and start to read from the " following href=
        (https?:        # match http(s): (s is optional)
        [^":]+?)        # match as few non-"-characters as possible and then "
        (?:\#.*?)?"     # read past without keeping anything following #
        .*?>.*?</a>     # match the end of the block
        """, re.VERBOSE)
    abs_matches = abs_urls.findall(text)
    abs_matches = list(set(abs_matches))    # remove duplicates

    matches = rel_matches + rel2_matches + abs_matches
    # just in case som absolutes and relatives were duplicates
    matches = list(set(matches))
    if output:
        with open(output + '.txt', 'w') as outfile:
            [outfile.write(match + '\n') for match in matches]
    return matches

def find_articles(url, output=None):
    """Return a list of all the Wikipedia articles linked to in the website of 
    the url given as input parameter.

    Args:
        url (str): url of the website to search for links to Wikipedia articles
        output (str, optional): path to file to which the matches will be saved

    Returns:
        articles (list of str objects): the links to all the Wikipedia articles 
            linked to in the website of the url given passed as input

    """
    resp = get_html(url)
    base = re.match(r'https?://\w+(?:\.\w+)*/', url).group(0)
    urls = find_urls(resp.text, base)

    wiki_pattern = re.compile(r'https?://\w+\.wikipedia.org')
    articles = []
    for url in urls:
        matched = wiki_pattern.match(url)
        is_match = bool(matched)
        if is_match:
            articles.append(url)

    if output:
        with open(output + '.txt', 'w') as outfile:
            [outfile.write(url + '\n') for url in articles]
    return articles

if __name__ == '__main__':
    urls = [
        'https://en.wikipedia.org/wiki/Nobel_Prize',
        'https://en.wikipedia.org/wiki/Bundesliga',
        'https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup'
    ]
    base = 'https://en.wikipedia.org/'
    fnames = ['nobel_prize', 'bundesliga', 'ski']

    for url, fname in zip(urls, fnames):
        fname = 'filter_urls/' + fname
        find_urls(req.get(url).text, base, fname + '_find_url')
        find_articles(url, fname + '_find_articles')
