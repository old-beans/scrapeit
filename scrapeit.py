#! python3

import requests
import pyperclip
import bs4
import re
import os, sys, errno

print(sys.path[0])
print(sys.argv)
os.chdir(sys.path[0])


# check for existence of folder, create if not
def create_folder():
    if not os.path.exists(os.path.dirname(folder)):
        try:
            os.makedirs(os.path.dirname(folder))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def make_soup(page_url):
    try:
        res = requests.get(page_url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        return soup

    except requests.exceptions.SSLError:
        print('SSL Error - ', page_url)
        return None
    except requests.exceptions.HTTPError:
        print('HTTP Error - ', page_url)
        return None


# write all text from page in lowercase to new .txt file
def write_text(soup, page_url, counter=None):
    if counter:
        filename = folder + str(counter) + '_scrape.txt'

    else:
        filename = folder + soup.title.text.strip() + '_scrape.txt'

    with open(filename, 'w') as f:
        f.write(page_url + '\n')
        f.write(soup.title.text + '\n\n')
        
        for string in soup.stripped_strings:
            
            try:
                f.write(string.lower() + '   ')
            except UnicodeEncodeError:
                print(page_url + "\nUnicode Error - foreign language detected")
                # In case of different language

    f.close()


def process_urls_from_txt(txt_file):
    # txt_file is .txt with urls separated by line
    create_folder()
    url_file = open(txt_file,'r')

    n = 1
    for url in url_file.readlines():
        if url[-1:] == '\n':
            url = url[:-1] # need to drop '\n' at end of url
        
        if 'http' in url:
            new_soup = make_soup(url)
            if  new_soup: 
                write_text(new_soup, url, counter=n)
                n += 1


def process_url():
    new_soup = make_soup(url)
    write_text(new_soup, url)

#################################################################


if len(sys.argv) > 1:

    if sys.argv[1] == 'file': # [scrapeit.py, file, filepath.txt]
        in_file = 'input\\' + sys.argv[2]
        keyword = sys.argv[2][:-4]
        folder = 'ouput\\' + keyword + '\\'
        process_urls_from_txt(in_file)

    # elif 'http' in sys.argv[1]: # [scrapeit.py, http://... or https://...]
    #     url = sys.argv[1:]
    #     folder = 'scrapeit text\\'
    #     create_folder()
    #     process_url()

else:
    # try:
    if 'http' in pyperclip.paste():
        url = pyperclip.paste()
        folder = 'scrapeit text\\'
        create_folder()
        process_url()

    else:
        print("no input url given. either copy address to clipboard or append 'file filename.txt' to run command")

print("bye")