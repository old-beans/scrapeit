#! python3

import requests
import pyperclip
import bs4
import re
import os, sys, errno
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
        folder + soup.title.text.strip() + '_scrape.txt'

    with open(filename, 'w') as f:
        f.write(page_url + '\n')
        f.write(soup.title.text + '\n\n')
        
        for string in soup.stripped_strings:
            
            try:
                f.write(string.lower())
            except UnicodeEncodeError:
                print(page_url + "\nUnicode Error - foreign language detected")
                # In case of different language

    f.close()


def process_urls_from_txt(txt_filepath):
    n = 1
    for url in txt_filepath.readlines():
        if url[-1:] == '\n':
            url = url[:-1] # need to drop '\n' at end of url
        
        if 'http' in url:
            new_soup = make_soup(url)
            if  new_soup: 
                write_text(new_soup, url, counter=n)
                n += 1


def process_url():
    create_folder()
    new_soup = make_soup(url)
    write_text(new_soup, url)


#################################################################

if len(sys.argv) > 2:

    if sys.argv[1] == 'file': # [scrapeit.py, 'file', filepath.txt]
        process_url_txt(sys.argv[2])        

elif 'http' in sys.argv[1]: # [scrapeit.py, http://... or https://...]
    url = sys.argv[1:]
    folder = 'scrapeit text\\'

else:
    url = pyperclip.paste()
    folder = 'scrapeit text\\'


create_folder()
new_soup = make_soup(url)
write_text(new_soup, url)
# url_file = open(url_filename,'r')

        # need to drop the '\\n' at the end of each line, hence [:-1]

print("bye")