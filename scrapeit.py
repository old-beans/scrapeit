#! python3

import requests
import bs4
import re
import os, sys, errno
os.chdir(sys.path[0])


# urls show only 
url_filename = 'forensics urls.txt'


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
def write_text(soup, page_url, counter):

    with open(folder + str(counter) + '_scrape.txt', 'w') as f:
        f.write(page_url)
        f.write(soup.title.text + '   ')
        
        for string in soup.stripped_strings:
            
            try:
                f.write(string.lower())
            except UnicodeEncodeError:
                print(page_url + "\nUnicode Error - foreign language detected")
                # In case of different language
    f.close()



#################################################################
# beginning of script

keyword = url_filename.split()[0]
folder = 'scraped text\\' + keyword + '\\'

create_folder()

url_file = open(url_filename,'r')

n = 1
for url in url_file.readlines():
    if url[-1:] == '\n':
        url = url[:-1] # need to drop '\n' at end of url
    
    if 'http' in url:
        new_soup = make_soup(url)
        if  new_soup: 
            write_text(new_soup, url,  n)
            n += 1

        # need to drop the '\\n' at the end of each line, hence [:-1]

print("bye")