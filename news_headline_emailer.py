import requests

from bs4 import BeautifulSoup

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
now = datetime.datetime.now()

content = ''

def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*100+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+ tag.text+'\n'+'<br>') if tag.text!='More' else '')
    return(cnt)

url = 'https://news.ycombinator.com/'

cnt = extract_news(url)
content += cnt
content += ('<br>-------<br>')
content += ('<br><br>End of Message')

print('Composing mail...')

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = ''
TO = ''
PASS = ''

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automate Email]'+' '+str(now.day)+'-'+str(now.month)+'-'+str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initializing Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
