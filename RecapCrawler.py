import urllib
import urllib.request
import os
from bs4 import BeautifulSoup

START_MATCH_ID_16 = 151595
END_MATCH_ID_16 = 152824
START_MATCH_ID_15 = 150126
END_MATCH_ID_15 = 151356

def getPage(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    req = urllib.request.Request(url, headers={
        'User-Agent': user_agent
    })
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')

def getRecap(match_id):
    url = 'https://nba.hupu.com/games/recap/' + str(match_id)
    html_result = getPage(url)

    soup = BeautifulSoup(html_result, "lxml")

    recap_name = soup.find('title').find(text=True)
    target_div = soup.find('div', {'class':"table_list_live"})

    recap_title = target_div.h2.find(text=True)
    recap_content = [p.find(text=True).replace(u'\xa0', u' ') for p in target_div.select("p")]

    return recap_name, recap_title, recap_content

match_id = START_MATCH_ID_15
while match_id <= END_MATCH_ID_15:
    print(match_id)
    try:
        recap_name, recap_head, recap_content = getRecap(match_id)
        recap_name = recap_name.replace('\n', '').replace("－虎扑NBA原创报道", "")
        file_name = recap_name + '.txt'
        file_path = os.path.abspath('./2015-16/Recap_15-16')
        local = os.path.join(file_path, file_name)

        f = open(local, 'w')
        f.write(recap_head + '\n')
        for p in recap_content:
            f.write(p + '\n')
        f.close()

        match_id += 1
    except:
        log_file = open(os.path.abspath('./2015-16/log_15-16.txt'), 'a')
        log_file.write(str(match_id) + '\n')
        log_file.close()

        match_id += 1