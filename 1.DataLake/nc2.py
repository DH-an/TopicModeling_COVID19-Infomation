import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from multiprocessing import Pool

query = '코로나'  # 검색어
start_date = '2020.07.01.'  # 검색 시작 날짜 (YYYYMMDD 형식)
end_date = '2020.12.31.'  # 검색 종료 날짜 (YYYYMMDD 형식)


def get_content(question_url):
    question_response = requests.get(question_url)
    question_soup = BeautifulSoup(question_response.text, 'html.parser')
    content = question_soup.select_one('div.c-heading__content')
    content_text = content.get_text(strip=True) if content is not None else ""
    return content_text

def scrape_page(page):
    url = f'https://kin.naver.com/search/list.naver?query={query}&period={start_date}:{end_date}&section=kin&page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for question in soup.select('#s_content > div.section > ul > li'):
        title = question.select_one('dt > a').text.strip()
        link = question.select_one('dt > a')['href']
        date = question.select_one('dd.txt_inline').text.strip()
        content_text = ""

        question_url = link
        results.append([title, link, date, content_text])

    # content_text는 멀티 프로세싱으로 처리하기
    with Pool(processes=4) as pool:
        contents = pool.map(get_content, [result[1] for result in results])
        for result, content in zip(results, contents):
            result[3] = content

    return results

if __name__ == '__main__':
    query = '코로나'  # 검색어
    start_date = '2020.07.01.'  # 검색 시작 날짜 (YYYYMMDD 형식)
    end_date = '2020.12.31.'  # 검색 종료 날짜 (YYYYMMDD 형식)

    url = f'https://kin.naver.com/search/list.nhn?sort=none&section=kin&query={query}&period={start_date}%7C{end_date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.select_one('#s_content > div.section > ul > li:nth-child(1) a')['href']
    print(link)

    # 총 페이지 수 구하기
    num_results = soup.select_one('#s_content > div.section > h2 > span > em').text
    num_results = num_results.split('/')[1].strip()
    num_results = int(num_results.replace(',', ''))
    last_page = -(-num_results // 10)  # 올림 계산
    print(f"페이지수:{last_page}")

    # 멀티프로세싱으로 크롤링하기
    results = []
    with Pool(processes=4) as pool:
        for result in tqdm(pool.imap_unordered(scrape_page, range(1, last_page + 1))):
            results.extend(result)

    # 결과를 CSV 파일로 저장하기
    with open('naverkin_crawling_20_2.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Link', 'Date', 'Content'])
        writer.writerows(results)
