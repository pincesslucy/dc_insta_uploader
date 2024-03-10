import openai
import configparser
import pandas as pd
from tabulate import tabulate

def get_hashtags(text):
    OPENAI_API_KEY = 'openai_api_key_here'
    openai.api_key = OPENAI_API_KEY
    messages = [{
        "role": "system",
        "content": "넌 글의 제목을 알려주면 제목과 관련된 인스타그램에 게시할 때 사용할 해시태그를 생성해주는 인공지능이야. 제목과 관련높은 단어로 딱 3개 이하로 단어형태로만 생성해. 오직 해시태그만 작성해"
    }, {
        "role": "user",
        "content": "'비행기 테러하겠다' 협박글 30대, 집행유예"
    }, {
        "role": "assistant",
        "content": "#비행기 #테러 #사회이슈"
    }, {
        "role": "user",
        "content": text
    }]
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def get_account_info():
    config = configparser.ConfigParser()
    config.read('config.ini')
    section = config.sections()
    df = pd.DataFrame(section, columns=['계정명'])

    q2 = input(f"{tabulate(df, headers='keys', tablefmt='psql')}\n계정을 선택하세요:")
    account = df.iloc[int(q2), 0]
    ACCOUNT_USERNAME = config[account]['USERNAME']
    ACCOUNT_PASSWORD = config[account]['PASSWORD']
    return ACCOUNT_USERNAME, ACCOUNT_PASSWORD