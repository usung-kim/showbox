import telegram
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

# 검색 키워드
search_word = '삼성전자'

#---------------------------텔레그램 봇 생성-------------------#
token = '1189588689:AAF_qhEDpkoEDKFMe2E3sTcuwf76wusCYtI'
bot = telegram.Bot(token=token)
# 스케쥴러 생성
sched = BlockingScheduler()
# 기존에 보냈던 링크를 담아둘 리스트
old_links = []

# 마지막 기사 제목만
old_subject = []

# 스크래핑 함수 (링크)
def extract_links(old_links=[]):
    # 해당 url의 html문서를 soup 객체로 저장
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')  # select_one() 함수는: 처음으로 발견한 하나의 엘리먼트만 반환합니다 -> 삼성전자 뉴스결과 전체를 갖음
    news_links = search_result.select('.bx > .news_wrap > a')  # select() 함수는 발견한 모든 엘리먼트를 리스트 형식으로 반환합니다.

    one_save = []
    for news in news_links:
        link=news['href']
        one_save.append(link)

    two_save=[]
    for one_link in one_save:
        if one_link not in old_links:
            two_save.append(one_link)
    return two_save

# 스크래핑 함수 (제목)
def extract_subject(old_subject=[]):
    # 해당 url의 html문서를 soup 객체로 저장
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')  # select_one() 함수는: 처음으로 발견한 하나의 엘리먼트만 반환합니다 -> 삼성전자 뉴스결과 전체를 갖음
    news_subject = search_result.select('.bx > .news_wrap > a')  # select() 함수는 발견한 모든 엘리먼트를 리스트 형식으로 반환합니다.

    one_subsave = []
    for news in news_subject:
        subject = news.get_text()
        one_subsave.append(subject)

    two_subsave = []
    for one_subject in one_subsave:
        if one_subject not in old_subject:
            two_subsave.append(one_subject)

    return two_subsave

# 텔레그램 메시지 전송 함수
def send_links():
    global old_links
    global old_subject

    # func: extract_links(old_links)
    new_links = extract_links(old_links)
    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id='1369159757', text=link)
    else:
        bot.sendMessage(chat_id='1369159757', text='새로운 뉴스 없음')
    old_links += new_links.copy()
    old_links = list(set(old_links))

    # func: extract_subject(old_subject)
    old_subject = extract_subject(old_subject)
    if old_subject:
        for subject in old_subject:
            bot.sendMessage(chat_id='1369159757', text=subject)
    else:
        bot.sendMessage(chat_id='1369159757', text='요약없음')
    old_subject += old_subject.copy()
    old_subject = list(set(old_subject))


# 최초 시작
send_links()
# 스케쥴러 세팅 및 작동
sched.add_job(send_links, 'interval', hours=1)
sched.start()




    #bot.sendMessage(chat_id='1369159757', text=result)

#for i in bot.getUpdates():
#    print(i.message)

#bot.sendMessage(chat_id='1369159757', text='쓰고 싶은 말')

# https://api.telegram.org/bot1189588689:AAF_qhEDpkoEDKFMe2E3sTcuwf76wusCYtI/getUpdates
# id":1369159757

# https://api.telegram.org/bot[봇토큰]/sendmessage?chat_id=[챗아이디]&text=[보낼메시지]
# https://api.telegram.org/bot1189588689:AAF_qhEDpkoEDKFMe2E3sTcuwf76wusCYtI/sendmessage?chat_id=1369159757&text=test
# result=print(i.get_text() + i['href'] + "\n")
