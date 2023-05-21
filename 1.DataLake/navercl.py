import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

query = '코로나'  # 검색어
start_date = '2022.01.01.'  # 검색 시작 날짜 (YYYYMMDD 형식)
end_date = '2022.06.30.'  # 검색 종료 날짜 (YYYYMMDD 형식)

url = f'https://kin.naver.com/search/list.nhn?sort=none&section=kin&query={query}&period={start_date}%7C{end_date}'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

link = soup.select_one('#s_content > div.section > ul > li:nth-child(1) a')['href']
print(link)

# 총 페이지 수 구하기
# num_results = soup.select_one('#s_content > div.section > h2 > span > em').text
# num_results = num_results.split('/')[1].strip()
# num_results = int(num_results.replace(',', ''))
# last_page = -(-num_results // 10) # 올림 계산
# print(f"페이지수:{last_page}")


# 각 페이지에서 질문 제목, 링크, 작성일자 정보 가져오기
results = []
with requests.Session() as session:  # 세션 사용
    for page in tqdm(range(1, 505)):
        url = f'https://kin.naver.com/search/list.naver?query={query}&period={start_date}:{end_date}&section=kin&page={page}'
        response = session.get(url)  # 세션에서 get 요청 보내기
        soup = BeautifulSoup(response.text, 'html.parser')

        for question in soup.select('#s_content > div.section > ul > li'):
            title = question.select_one('dt > a').text.strip()
            link = question.select_one('dt > a')['href']
            date = question.select_one('dd.txt_inline').text.strip()

            question_url = link
            question_response = session.get(question_url)  # 세션에서 get 요청 보내기
            question_soup = BeautifulSoup(question_response.text, 'html.parser')
            content = question_soup.select_one('div.c-heading__content')
            content_text = content.get_text(strip=True) if content is not None else ""

            results.append([title, link, date, content_text])

#print(results)

# 결과를 CSV 파일로 저장하기
with open('naver_kin_crawling22_1.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Link', 'Date'])
    writer.writerows(results)
