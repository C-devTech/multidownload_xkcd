#! python3
# multidownload_xkcd.py - Downloads XKCD comics using multiple threads..

import bs4
import os
import requests
import sys
import threading

os.makedirs('d:\\xkcd', exist_ok=True)     # Store comics in D:\XKCD

def download_xkcd(start_comic, end_comic):
    for url_number in range(start_comic, end_comic):
        try:
            url = 'http://xkcd.com/%s/' % (url_number)
            # Download the page
            print('Downloading page %s...' % url)
            res = requests.get(url)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            # Find the URL of the comic image.
            # Only select img within element with id attribute set to comic
            comic_elem = soup.select('#comic img')
            if comic_elem == []:
                print('Could not find comic image.')
            else:
                comic_url = 'http:' + comic_elem[0].get('src')
                # Download the image.
                print('Downloading the image %s...' % (comic_url))
                res = requests.get(comic_url)
                res.raise_for_status()

                # Save the image to d:\\xkcd
                with open(os.path.join('d:\\xkcd', \
                        os.path.basename(comic_url)), 'wb') as image_file:
                    for chunk in res.iter_content(100000):
                        image_file.write(chunk)
        except Exception:
            print('Error: ', sys.exc_info()[0], ' - ', sys.exc_info()[1])

# Create and start the Thread objects.
download_threads = []                   # A list of all the Thread objects
for i in range(0, 1400, 100):           # Loops 14 times, creates 14 threads...
    download_thread = threading.Thread(target=download_xkcd, args=(i, i+99))
    download_threads.append(download_thread)
    download_thread.start()

# Wait for all threads to end
for download_thread in download_threads:
    download_thread.join()

print('Done.')

