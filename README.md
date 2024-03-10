# DC 실시간베스트 게시물 instagram 업로드 자동화
---

인스타그램에서 자주 보이는 유머, 이슈 글들을 자동 업로드하는 프로그램입니다.
DC인사이드의 실시간 베스트 게시물의 이미지들을 수집해 썸네일과 해시태그를 자동으로 업로드합니다.

---
# Usage
1. python version 3.10 환경 준비
2. requirements 설치 및 실행
   ```python
   pip install requirements.txt
   ```
3. 인스타 계정 정보 입력
   config.ini 에서 계정 이름 및 패스워드 입력
4. 썸네일 폰트 경로 설정
   crawling.py의 line89의 font path 입력
5. 해시태그 자동 생성을 위한 gpt api 입력
   util.py의 line7에 openai api key 입력
6. RUN!
   ```python
   python main.py
   ```
   이후 클로링 옵션 선택 및 업로드 게시물 선택 안내에 따라 진행

# Result example
![화면 캡처 2024-03-10 195624](https://github.com/pincesslucy/dc_insta_uploader/assets/98650288/bcacb4fa-0e90-4acf-bd75-b26ee790765b)
![화면 캡처 2024-03-10 195733](https://github.com/pincesslucy/dc_insta_uploader/assets/98650288/ab13de28-fcc3-4b48-869a-fdccf2fdf3ad)
