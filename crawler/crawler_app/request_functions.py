import requests
from bs4 import BeautifulSoup
from collections import deque
import time
import urllib.robotparser as urobot
import validators
from requests.exceptions import RequestException
        
def status_code(url) -> int:
    try:
        r = requests.get(url)
        return r.status_code
    except RequestException as e:
        return 0

def text_response(url) -> str:
    r = requests.get(url)
    return r.text

def get_articles(url):
    html_content = text_response(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.find_all('a', class_='topic-article-link')

def is_valid_url(url):
    return validators.url(url)

def does_exist_robots_txt(url) -> bool:
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False
    
def parse_robots_txt(url):
    r = requests.get(url)
    print(r.text)

def check_robots_txt(url) -> bool:
    url_robots_txt = url+'/robots.txt'
    if does_exist_robots_txt(url_robots_txt):
        robots_url = urobot.RobotFileParser(url = url_robots_txt)
        robots_url.read()
        rrate = robots_url.request_rate("*")
        robots_url.crawl_delay("*")
        print(robots_url.can_fetch("*", url))
        return robots_url.can_fetch("*", url)
    else:
        print(f"{url_robots_txt} doesn't exist")
        return False

def check_access(url):
        return status_code(url) == 200 and check_robots_txt(url)

# с очередью из всех ссылок на странице
def crawl(start_url):
    domain = 'https://www.wikipedia.org/'
    visited = set()
    queue = deque([start_url])
    while queue:
        if len(visited) >= 10:
                        break
        url = queue.popleft()
        if url not in visited:
            visited.add(url)
            if status_code(url) == 200:
                html_content = text_response(url)
                soup = BeautifulSoup(html_content, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                for link in links:
                    if not is_valid_url(link):
                        if link not in visited and status_code(domain + link) == 200:
                                queue.append(domain + link)
                                visited.add(domain + link)
                    if link not in visited and is_valid_url(link):
                        if status_code(link) == 200:
                            if domain in link: # не уходить с вики
                                queue.append(link)
                                visited.add(link)
                    print(len(visited))
                    if len(visited) >= 10:
                        break
            time.sleep(1)
    return visited

# переход по первой попавшейся ссылке
# def crawl(start_url):
#     domain = 'https://www.wikipedia.org/'
#     domain_parts = ['https://', 'wikipedia.org']
#     visited = set()
#     is_added = False
#     url = start_url
#     # print(url)
#     i = 0
#     while len(visited) <= 3:
#         if not is_valid_url(url):
#             if url not in visited and status_code(domain + url) == 200:
#                     url = domain + url
#                     visited.add(url)
#                     is_added = True
#         if url not in visited and is_valid_url(url):
#             if status_code(url) == 200:
#                 if domain_parts[0] in url and domain_parts[1] in url: # не уходить с вики
#                     visited.add(url)
#                     is_added = True
#         if is_added:
#             print('added')
#             html_content = text_response(url)
#             soup = BeautifulSoup(html_content, 'html.parser')
#             is_added = False
#             links = [a['href'] for a in soup.find_all('a', href=True)]
#             if links != None:
#                 url = links[i]
#                 i += 1
#             else:
#                 break
#         else:
#             url = links[i]
#             i += 1
        
#         time.sleep(1)
#     return visited