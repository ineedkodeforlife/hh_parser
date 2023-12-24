import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE = "https://hh.ru/search/vacancy"
SEARCH_PARAMS = {"text": "Подработка", "area": 1}

headers = {
    "Host": "hh.ru",
    "User-Agent": "Safari",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def extract_max_page():
    r = requests.get(URL_TEMPLATE, params=SEARCH_PARAMS, headers=headers)
    pages = []
    if r.status_code == 200:
        bss = bs(r.text, "html.parser")
        paginator_not_in_range = bss.find_all("span", {"class": "pager-item-not-in-short-range"})
        for page in paginator_not_in_range:
            pages.append(int(page.find("a").text))

    return pages[-1]

def extract_hh_jobs(last_page):
    for page in range(0, last_page):
        params = {"text": "Подработка", "area": 1, "page": page}
        result = requests.get(URL_TEMPLATE, params=params, headers=headers)
        soup = bs(result.text, 'html.parser')
        results = soup.find_all('div', {'class' : 'vacancy-serp-item__layout'})
        for res in results:
            title = res.find('a').text
            vacancy_link = res.find('a').get('href')
            salary = res.find('span', {'class': 'bloko-header-section-2'})
            if salary != None:
                print(salary.text)
            company_link = res.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a')
            company = res.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').text
            print(title,'\n', company)
            print(vacancy_link + '\n')

