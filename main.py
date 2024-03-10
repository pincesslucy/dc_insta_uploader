from crawling import *
from tabulate import tabulate
import pandas as pd
from instagrapi import Client
from utils import *
import os
import webbrowser

def main():
    q = input('실베글 크롤링:0, 직접 입력:1 ')
    if q == '0':
        posts_num = int(input('몇 개의 게시글을 출력하시겠습니까? '))
        df = get_dc_best(posts_num)
        while True:
            print(tabulate(df, headers='keys', tablefmt='psql'))
            n = int(input('몇 번의 게시글의 이미지를 저장하시겠습니까? '))
            org_title = df.iloc[n]['title']
            url = df.iloc[n]['link']
            webbrowser.open(url)
            q1 = input('이 게시글의 이미지를 저장하시겠습니까? (y/n) ')
            if q1 == 'y':
                result = get_images(url, org_title)
                break
            else:
                continue

    elif q == '1':
        url = input('url을 입력하세요: ')
        org_title = get_title(url)
        result = get_images(url, org_title)
    
    if result:
        yesorno = input('인스타그램에 게시하시겠습니까? (y/n) ')

        if yesorno == 'y':
            ACCOUNT_USERNAME, ACCOUNT_PASSWORD = get_account_info()
            title = re.sub('[^ㄱ-ㅎa-zA-Z가-힣0-9 .!~?\u4E00-\u9FFF]', '', org_title)
            image_dir = f'./images/{title}/'
            files = os.listdir(image_dir)
            image_files = [file for file in files if file.endswith('.jpg') or file.endswith('.png')]
            image_paths = [image_dir + file for file in image_files]
            cl = Client()
            cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
            hashtags = get_hashtags(title)
            cl.album_upload(image_paths[:10],
                            caption=f"{org_title}\n.\n.\n{hashtags} #유머 #개그 #웃긴사진 #웃긴글 #웃긴짤 #빵터짐 #오늘의유머 #이슈 #뉴스 #10대 #20대 #30대 #꿀잼 #소통 #유머스타그램")
            print('게시 완료')
    else:
        print('사진 저장 실패')
if __name__ == '__main__':
    main()