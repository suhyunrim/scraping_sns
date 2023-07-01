import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook

def executeTwitter(twitter_id: str, date_from: str, date_to: str):
    os.system("taskkill /IM chrome.exe /F")

    os.startfile(f"execute_chrome.bat")

    chromedriver_path = './chromedriver.exe'
    twitter_profile_url = f'https://twitter.com/{twitter_id}'

    options = Options()
    options.add_argument("--start-maximized")  # 전체화면으로 실행
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(twitter_profile_url)

    date_from_obj = datetime.strptime(date_from, '%Y.%m.%d')
    date_to_obj = datetime.strptime(date_to, '%Y.%m.%d')

    time.sleep(3)

    tweets = []
    date_obj = None

    def toInt(str):
        if str == '':
            return 0
        else:
            return int(str.replace(',', ''))

    cacheTweets = set()

    scrollIdx = 1
    while True:
        tweet_elements = driver.find_elements(By.CLASS_NAME, 'css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu')
        for tweet in tweet_elements:
            date = tweet.find_element(By.CLASS_NAME, 'css-4rbku5.css-18t94o4.css-901oao.r-14j79pv.r-1loqt21.r-xoduu5.r-1q142lx.r-1w6e6rj.r-37j5jr.r-a023e6.r-16dba41.r-9aw3ui.r-rjixqe.r-bcqeeo.r-3s2u2q.r-qvutc0')
            url = date.get_attribute('href')

            if url in cacheTweets:
                continue

            dateText = date.text

            if dateText == '':
                alarm_elements = driver.find_elements(By.CLASS_NAME, 'css-18t94o4.css-1dbjc4n.r-1niwhzg.r-1ets6dv.r-sdzlij.r-1phboty.r-rs99b7.r-1wzrnnt.r-19yznuf.r-64el8z.r-1ny4l3l.r-1dye5f7.r-o7ynqc.r-6416eg.r-lrvibr')
                if alarm_elements:
                    alarm_elements[0].click()
                break

            # 트윗 날짜 확인
            if '시간' in dateText or '분' in dateText or '초' in dateText:
                date_obj = datetime.now()
            elif '년' in dateText:
                date_obj = datetime.strptime(dateText, '%Y년 %m월 %d일')
            else:
                dateText = f'{datetime.now().year}년 {dateText}'
                date_obj = datetime.strptime(dateText, '%Y년 %m월 %d일')
                
            if date_obj == None:
                break

            if date_obj > date_to_obj:
                continue

            if date_obj < date_from_obj:
                break

            cacheTweets.add(url)

            title = ''
            # 내용이 없는 트윗도 있음
            if tweet.find_elements(By.CLASS_NAME, 'css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0'):
                title = tweet.find_element(By.CLASS_NAME, 'css-901oao.r-18jsvk2.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0').text.strip()

            counts = tweet.find_elements(By.CLASS_NAME, 'css-901oao.css-16my406.r-poiln3.r-n6v787.r-1cwl3u0.r-1k6nrdp.r-1e081e0.r-qvutc0')
            comment_Count = toInt(counts[0].text)
            retweet_count = toInt(counts[1].text)
            sympathy_Count = toInt(counts[2].text)
            read_count = toInt(counts[3].text)

            tweets.append({
                'Title': title,
                'Month': date_obj.month,
                'Day': date_obj.day,
                'URL': url,
                'RetweetCount': retweet_count,
                'ReadCount': read_count,
                'SympathyCount': sympathy_Count,
                'CommentCount': comment_Count})

        # 기간 초과
        if date_obj < date_from_obj:
            break

        # 마지막까지 도달함
        if driver.find_elements(By.CLASS_NAME, 'scroll_top_button__ntlo_'):
            break;

        # 스크롤 내리기
        driver.execute_script(f'window.scrollTo(0, document.body.clientHeight * {scrollIdx});')
        scrollIdx = scrollIdx + 1

        time.sleep(3)

    # 크롬 드라이버 종료
    driver.quit()

    # 추출한 포스팅을 엑셀 파일로 저장
    wb = Workbook()
    ws = wb.active

    #헤더 추가
    ws.append(['No.', '월', '일자', '내용', 'URL', '구분', '제작', '노출', '참여', '비고'])

    tweets.reverse()

    # 포스팅 데이터 추가
    for post in tweets:
        ws.append(['',
                    f'{post["Month"]}월',
                    f'{post["Day"]}일',
                    post['Title'],
                    post['URL'],
                    '',
                    '',
                    post['ReadCount'],
                    post['SympathyCount'] + post['CommentCount'] + post['RetweetCount'],
                    ''
                ])

    # 엑셀 파일 저장
    excel_file_name = f'twitter_{twitter_id}_{date_from.replace(".", "-")}_{date_to.replace(".", "-")}.xlsx'
    wb.save(excel_file_name)

    print(f'Excel 파일이 생성되었습니다: {excel_file_name}')
    os.system("taskkill /IM chrome.exe /F")