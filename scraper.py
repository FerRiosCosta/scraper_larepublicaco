import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, dir_news):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(XPATH_TITLE)[1]
                title = title.replace('\"', '')
                
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{dir_news}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            dir_news = "news_" + today
            if not os.path.isdir(dir_news):
                os.mkdir(dir_news)

            for link in links_to_notices:
                parse_notice(link, dir_news)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    
def run():
    parse_home()


if __name__ == '__main__':
    run()


