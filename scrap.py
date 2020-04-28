import requests
import ssl
import slack
import os
import pandas as pd
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

def scrap_web(type):
    url = "https://www.mohfw.gov.in/"
    req=requests.get(url)
    page_soup = soup(req.content,"html.parser")
    
    corona_status = page_soup.find_all("div",{"class":"site-stats-count"})
    tags=corona_status[0].find_all("li")

    state_chart = page_soup.find_all("table" ,{"class":"table-striped"})
    
    if type == 'grids':
        return tags
    elif type == 'table':
        return state_chart

def convert_map_to_(): 
    state_chart = scrap_web('table')
    state_data = state_chart[0].find_all("tr")

    table_list=[]

    for one_by_one in state_data:
        row = {}
        if len(one_by_one.find_all("td"))==5:
            row["S. No."] = one_by_one.find_all("td")[0].text
            row["Name of State / UT"] = one_by_one.find_all("td")[1].text
            row["Total Confirmed cases (Including 71 foreign Nationals)"] = one_by_one.find_all("td")[2].text
            row["Cured/Discharged/Migrated"] = one_by_one.find_all("td")[3].text
            row["Death"] = one_by_one.find_all("td")[4].text
            table_list.append(row)
        else:
            pass
    df = pd.DataFrame(table_list)

    return row

def convert_map_to_table():
    html_body_code=get_html()

    table_data=convert_map_to_()
    print(table_data)
    html_table_tag='<table>'
    for row in table_data :
        html_table_tag = html_table_tag + '<tr>'
        for data in row.values():
            html_table_tag = html_table_tag + '<td>' + data + '</td>'
        html_table_tag = html_table_tag + '</tr>'
    html_table_tag= html_table_tag + '</table>'

    complete_html=html_body_code.replace('[ADD_TABLE]',html_table_tag)
    print(complete_html)
    send_mail(complete_html)

def get_html():
    return '''<html> 
    <head>
    <style>
         .site-stats-count{
            text-align: center;

         }

         ul{
             list-style: none;
             display:flex;
         }
         li{
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

def generate_html():
    tags = scrap_web('grids')
    corona_cases = {}
    for tag in tags:
        try:
            corona_cases[tag.find('span').text]=tag.find('strong').text
        except:
            pass

    html_data='<ul>'
    for key in corona_cases:
        html_data = html_data + '<li><strong>' + corona_cases[key] + '</strong>'
        html_data = html_data + '<span>' + key + '</span></li>'
    html_data=html_data+'</ul>'

    html_code=get_html()
    # Turn these into plain/html MIMEText objects
    html=html_code.replace('[ADD_TABLE]',html_data)
    print(html)
    send_mail(html)

def send_mail(html_data):
    port = read_property('server_details', 'port')
    smtp_server = read_property('server_details', 'smtp.server')
    sender_email = read_property('sender_credentials', 'sender.email')
    receiver_email = read_property('receiver_details', 'receiver.email')
    password = os.environ.get('PASSWORD')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    #message.attach(part1)
    message = MIMEMultipart("alternative")
    message["Subject"] = "COVID-19 INDIA"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(html_data,"html"))

    #Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('Email Sent to',receiver_email)
    except SMTPException:
        print('ERROR: Problem in sending mail')

def send_to_slack():
    SLCK_API_TOKEN = 'xoxp-1038956771587-1038956771683-1045110021895-894f5ac66a38b3b45738329bf9e9b097'
    client = slack.WebClient(token = SLCK_API_TOKEN)
    try:
        response = client.chat_postMessage(channel='#automation-call',text=message.as_string())
        assert response["ok"]
        assert response["message"]["text"] == message.as_string()
    except:
        print('ERROR: Please check if the message posted to slack!')

if __name__ == '__main__':
    generate_html()
    #print(read_property('sender_credentials', 'sender.email'))