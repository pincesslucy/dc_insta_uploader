import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib import request
import os
from tqdm import tqdm
import re
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def get_title(url):
    response = requests.get(url, headers={'User-agent': ''})
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('span', {'class': 'title_subject'}).text
    return title

def get_dc_best(num, page_num=1):
    url = 'https://www.dcinside.com/'
    
    titles = []
    categories = []
    links = []

    while num > 0:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for i in range(2, num + 2):
            try:
                title = soup.select_one(f'#dcbest_list_date > ul.typet_list.p_{page_num} > li:nth-child({i}) > a > div.box.besttxt > p').text
                titles.append(title)
                category = soup.select_one(f'#dcbest_list_date > ul.typet_list.p_{page_num} > li:nth-child({i}) > a > div.box.best_info > span.name').text
                categories.append(category)
                link = soup.select_one(f'#dcbest_list_date > ul.typet_list.p_{page_num} > li:nth-child({i}) > a').get('href')
                links.append(link)
                num -= 1
            except:
                break
        page_num += 1

    return pd.DataFrame({'title': titles, 'category': categories, 'link': links})

def get_images(url, title):
    response = requests.get(url, headers={'User-agent': ''})
    soup = BeautifulSoup(response.text, 'html.parser')
    title = re.sub('[^ㄱ-ㅎa-zA-Z가-힣0-9 .!~?\u4E00-\u9FFF]', '', title)
    images = soup.find('div', {'class': 'appending_file_box'}).find_all('li')
    img_urls = [img.find('a', href=True)['href'] for img in images]

    os.makedirs('./images/' + title, exist_ok=True)
    make_thumbnail(title)
    for i, img_url in tqdm(enumerate(img_urls)):
        opener = request.build_opener()
        opener.addheaders = [('User-agent', ''), ('Referer', response.url)]
        request.install_opener(opener)
        request.urlretrieve(img_url, f'./images/{title}/img_{str(i+1).zfill(2)}.jpg')
        img = Image.open(f'./images/{title}/img_{str(i+1).zfill(2)}.jpg')
        # Get the larger dimension
        max_dim = max(img.size)
        # Create a new white image with the larger dimension
        new_img = Image.new("RGB", (max_dim, max_dim), (255, 255, 255))
        # Paste the original image to the center of the new image
        new_img.paste(img, ((max_dim - img.size[0]) // 2, (max_dim - img.size[1]) // 2))
        # Save the new image
        new_img.save(f'./images/{title}/img_{str(i+1).zfill(2)}.jpg')
    print('이미지 저장 완료')
    return True


def make_thumbnail(title):
    pink = (255, 192, 203)
    # 500x500 크기의 하얀색 이미지 생성
    image = np.full((500, 500, 3), pink, dtype=np.uint8)

    # 이미지를 PIL 형식으로 변환
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # draw 객체 생성
    draw = ImageDraw.Draw(image_pil)

    # 텍스트를 8글자 단위로 분할
    lines = [title[i:i+8] for i in range(0, len(title), 8)]
    line_spacing = 50
    font_size = 50
    if len(lines) > 4:
        font_size = 30
        line_spacing = 30
    font = ImageFont.truetype('*********font path****', font_size)
    total_text_height = len(lines) * (draw.textbbox((0, 0), title, font=font)[3] - draw.textbbox((0, 0), title, font=font)[1]) + (len(lines) - 1) * line_spacing

    # 각 줄에 대해 텍스트 그리기
    for i, line in enumerate(lines):
        # 텍스트의 크기 및 오프셋 계산
        text_width = draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0]
        text_height = draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        width, height = image_pil.size
        x = (width - text_width) // 2
        y = (height - total_text_height) // 2 + i * (text_height + line_spacing)

        # 텍스트 그리기 (텍스트 위치와 내용, 색상, 글꼴을 설정)
        draw.text((x, y), line, font=font, fill=(0, 0, 0))

    # save the image
    image_pil.save(f'./images/{title}/img_0.jpg')