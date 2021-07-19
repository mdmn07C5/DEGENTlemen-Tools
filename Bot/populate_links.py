from bs4 import BeautifulSoup
from pathlib import Path
import inspect, requests, pprint
# just to populate links once


end_point = 'https://knowyourmeme.com/memes/apu-apustaja/photos/'
headers = { 'user-agent':'curl/7.55.1'}

response = requests.get(url=end_point, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
pagination_result_set = soup.find(class_='pagination').find_all('a')

# pagination_result_set contains a truncated list of pages, because the last
# item is a link to the next page, we're taking the next to last (-2) to get
# the last page, also find_all returns a generator which is why we use next()
last_page = next(pagination_result_set[-2].stripped_strings)

img_tags = []

for page in range(int(last_page)+1):
    # for page in range(2):
    print(f'parsing page {page}')
    url = f'https://knowyourmeme.com/memes/apu-apustaja/photos/page/{page}'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    photo_gallery_div = soup.find(id='photo_gallery')
    img_tags.extend(photo_gallery_div.find_all('img'))

# create a list only containing the data-src attribute which will contain the
# thumbnail link, some of them will be promotional images with 'promotionals'
# in the link instead of 'photos'
thumbnail_links = [
    img['data-src'] for img in img_tags if 'photos' in img['data-src']
]

# replace 'masonry' with 'original' in the links to get full image
photo_links = [
    link.replace('masonry', 'original') for link in thumbnail_links
]

path = Path(__file__).parent
with open(path/'apu_links.txt', 'w') as f:
    for link in photo_links:
        f.write(link+'\n')