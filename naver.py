import os
import time

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook

def executeNaver(naver_id: str, date_from: str, date_to: str):
    os.system("taskkill /IM chrome.exe /F")

    os.startfile(f"execute_chrome.bat")

    chromedriver_path = 'chromedriver.exe'
    blog_url = f'https://m.blog.naver.com/{naver_id}?categoryNo=0&listStyle=card'

    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(blog_url)

    date_from_obj = datetime.strptime(date_from, '%Y.%m.%d')
    date_to_obj = datetime.strptime(date_to, '%Y.%m.%d') + timedelta(days=1) - timedelta(seconds=1)

    time.sleep(3)

    posts = []
    date_obj = None

    while True:
        length = len(driver.find_elements(By.CLASS_NAME, 'card__WjujK'))
        for i in range(length):
            post_elements = driver.find_elements(By.CLASS_NAME, 'btn_close._btn_close')
            if post_elements:
                post_elements[0].click()

            post_elements = driver.find_elements(By.CLASS_NAME, 'card__WjujK')
            element = post_elements[i]

            date = element.find_element(By.CLASS_NAME, 'time__MHDWV').text.strip()

            if '시간' in date or '분' in date or '초' in date:
                date_obj = datetime.now()
            else:
                date_obj = datetime.strptime(date, '%Y. %m. %d.')

            if date_obj > date_to_obj:
                continue

            if date_obj < date_from_obj:
                break

            title = element.find_element(By.CLASS_NAME, 'title__tl7L1.ell2')
            titleText = title.text.strip()

            fullUrl = element.find_element(By.CLASS_NAME, 'link__iGhdI').get_attribute('href')
            urlSplit = fullUrl.split('&')
            url = f'https://blog.naver.com/{naver_id}/{urlSplit[1][6:]}'

            read_count = ''
            if element.find_elements(By.CLASS_NAME, 'count__tpBXw'):
                read_count = int(element.find_element(By.CLASS_NAME, 'count__tpBXw').text.split(' ')[0])

            sympathy_Count = ''
            if element.find_elements(By.CLASS_NAME, 'u_cnt._count'):
                sympathy_Count = int(element.find_element(By.CLASS_NAME, 'u_cnt._count').text.strip())

            comment_Count = ''
            if element.find_elements(By.CLASS_NAME, 'comment_btn__lcx93'):
                comment_Count = int(element.find_element(By.CLASS_NAME, 'comment_btn__lcx93').text.strip())

            driver.get(url)

            time.sleep(1.5)

            driver.switch_to.frame('mainFrame')
            category = driver.find_element(By.ID, 'selectedMenu').text

            driver.execute_script("window.history.go(-1)")

            time.sleep(1.5)

            posts.append({
                'Title': titleText,
                'Month': date_obj.month,
                'Day': date_obj.day,
                'URL': url,
                'Category': category,
                'ReadCount': read_count,
                'SympathyCount': sympathy_Count,
                'CommentCount': comment_Count})

        if date_obj < date_from_obj:
            break

        if driver.find_elements(By.CLASS_NAME, 'scroll_top_button__ntlo_'):
            break;

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)

    driver.quit()

    wb = Workbook()
    ws = wb.active

    ws.append(['No.', '월', '일자', '내용', 'URL', '구분', '카테고리', '제작', '공감', '댓글', '참여', '조회 수', '비고'])

    posts.reverse()

    rowCount = 1
    for post in posts:
        ws.append(['',
                    f'{post["Month"]}월',
                    f'{post["Day"]}일',
                    post['Title'],
                    post['URL'],
                    '원고',
                    post['Category'],
                    '레인보우',
                    post['SympathyCount'],
                    post['CommentCount'],
                    post['SympathyCount'] + post['CommentCount'],
                    post['ReadCount'],
                    ''])
        rowCount = rowCount + 1
        urlCell = ws[f'E{rowCount}']
        urlCell.hyperlink = post['URL']
        urlCell.style = "Hyperlink"

    excel_file_name = f'naver_{naver_id}_{date_from.replace(".", "-")}_{date_to.replace(".", "-")}.xlsx'
    wb.save(excel_file_name)

    print(f'Excel 파일이 생성되었습니다: {excel_file_name}')
    os.system("taskkill /IM chrome.exe /F")