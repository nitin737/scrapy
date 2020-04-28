import requests
import ssl
import slack
import configparser as parser
from bs4 import BeautifulSoup as soup
from smtplib import SMTP_SSL,SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_property(section, key):
    config = parser.RawConfigParser()
    config.read('user.properties')
    value = config.get(section, key)
    return value

def scrap_web():
    url = "https://www.mohfw.gov.in/"
    req=requests.get(url)
    page_soup = soup(req.content,"html.parser")
    corona_status = page_soup.find_all("div",{"class":"site-stats-count"})
    tags=corona_status[0].find_all("li")

    corona_cases={}

    for tag in tags:
        try:
            corona_cases[tag.find('span').text]=tag.find('strong').text
        except:
            pass
    return corona_cases


def get_html():
    text = '''<html> 
    <head>
    <style>
         .site-stats-count{
            text-align: center;

         }

         ul{
             list-style: none;
         }
         li{
            display:block;
            margin:10px;
            width:130px;
            height:80px;
            border-radius:5px;

            background-image: linear-gradient(rgb(197, 99, 99), rgb(137, 199, 126));
         }

         strong{
            display:block;
             font-weight:bold;
             padding:8px 2px 0px 2px;
             font-size:16pt;
         }

         span{
            display:block;
            padding:2px;
            font-size:13pt;
         }
    </style>
    </head>
    <body>
    <div class="site-stats-count">
    [ADD_TABLE]
    </div>
    </body>
    </html>'''
    return text


def generate_replace_html():
    html_data='<ul>'
    corona_cases = scrap_web()
    for key in corona_cases:
        html_data = html_data + '<li><strong>' + corona_cases[key] + '</strong>'
        html_data = html_data + '<span>' + key + '</span></li>'
    html_data=html_data+'</ul>'

    html_code=get_html()
    # Turn these into plain/html MIMEText objects
    html=html_code.replace('[ADD_TABLE]',html_data)
    send_mail(html)


def send_mail(html):
    port = 465 # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "mordor127001@gmail.com"
    receiver_email = "procomtech737@gmail.com"
    password = input("Type your password and press enter: ")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    #message.attach(part1)
    message = MIMEMultipart("alternative")
    message["Subject"] = "COVID-19 INDIA"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(html,"html"))

    #Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('Email Sent to',receiver_email)
    except SMTPException:
        print('ERROR')



def send_to():
    SLCK_API_TOKEN = 'xoxp-1038956771587-1038956771683-1045110021895-894f5ac66a38b3b45738329bf9e9b097'
    client = slack.WebClient(token = SLCK_API_TOKEN)
    try:
        response = client.chat_postMessage(channel='#automation-call',text=message.as_string())
        assert response["ok"]
        assert response["message"]["text"] == message.as_string()
    except:
        print('ERROR: Please check if the message posted to slack!')

if __name__ == "__main__":
    #scrap_web()
    #generate_replace_html()
    print(read_property('sender_credentials', 'sender.email'))