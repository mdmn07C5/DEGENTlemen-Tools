from bs4 import BeautifulSoup
from pathlib import Path
import requests, random, pprint

pp = pprint.PrettyPrinter(indent=4)

def get_random_apu():
    request = requests.get('https://www.memeatlas.com/pepe-memes.html')
    soup = BeautifulSoup(request.content, 'html.parser')
    result_set = soup.find(id='list')

    results = []
    for result in result_set.contents:
        if (res := result.find('a')) != -1:
            results.append(res['href'])
    
    random.seed(None)
    random_apu = f'https://www.memeatlas.com/{random.choice(results)}'
    # return random_apu
    return requests.get(random_apu)

