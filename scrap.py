import configparser as parser
import os
import ssl
import html_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

import pandas as pd
import requests
import slack
from bs4 import BeautifulSoup as soup


def read_property(section, key):
    config = parser.RawConfigParser()
    config.read('user.properties')
    value = config.get(section, key)
    return value


def scrap_web(type):
    url = "https://www.mohfw.gov.in/"
    req = requests.get(url)
    page_soup = soup(req.content, "html.parser")

    corona_status = page_soup.find_all("div", {"class": "site-stats-count"})
    tags = corona_status[0].find_all("li")

    state_chart = page_soup.find_all("table", {"class": "table-striped"})

    if type == 'overall':
        return tags
    elif type == 'state-wise':
        return state_chart


def scrap_states_data():
    state_chart = scrap_web('state-wise')
    state_data = state_chart[0].find_all("tr")

    table_list = []

    for one_by_one in state_data:
        row = {}
        if len(one_by_one.find_all("td")) == 5:
            row["S. No."] = one_by_one.find_all("td")[0].text
            row["Name of State / UT"] = one_by_one.find_all("td")[1].text
            row["Total Confirmed cases (Including 71 foreign Nationals)"] = one_by_one.find_all(
                "td")[2].text
            row["Cured/Discharged/Migrated"] = one_by_one.find_all("td")[
                3].text
            row["Death"] = one_by_one.find_all("td")[4].text
            table_list.append(row)
        else:
            pass
    #df = pd.DataFrame(table_list)

    return row

def convert_to_html_table():  # call this method to tirgger state wise corona status
    html_body_code = html_template.get_html()

    table_data = scrap_states_data()

    html_table_tag = '<table>'
    for row in table_data:
        html_table_tag = html_table_tag + '<tr>'
        for data in row.values():
            html_table_tag = html_table_tag + '<td>' + data + '</td>'
        html_table_tag = html_table_tag + '</tr>'
    html_table_tag = html_table_tag + '</table>'

    complete_html = html_body_code.replace('[ADD_TABLE]', html_table_tag)

    send_mail(complete_html)


def generate_overall_status():  # call this method to trigger the overall india corona status
    tags = scrap_web('overall')
    corona_cases = {}
    for tag in tags:
        try:
            corona_cases[tag.find('span').text] = tag.find('strong').text
        except:
            pass

    html_data = '<ul>'
    for key in corona_cases:
        html_data = html_data + '<li><strong>' + \
            corona_cases[key] + '</strong>'
        html_data = html_data + '<span>' + key + '</span></li>'
    html_data = html_data+'</ul>'

    html_code = html_template.get_html()
    # Turn these into plain/html MIMEText objects
    html = html_code.replace('[ADD_TABLE]', html_data)

    send_mail(html)


def send_mail(html_data):
    port = read_property('server_details', 'port')
    smtp_server = read_property('server_details', 'smtp.server')
    sender_email = read_property('sender_credentials', 'sender.email')
    receiver_email = read_property('receiver_details', 'receiver.email')
    password = os.environ.get('PASSWORD')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message = MIMEMultipart("alternative")
    message["Subject"] = "COVID-19 INDIA"
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(html_data, "html"))

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('Email Sent to', receiver_email)
    except SMTPException:
        print('ERROR: Problem in sending mail')


def send_to_slack():
    SLCK_API_TOKEN = read_property('slack_api', 'slack.api.token')
    client = slack.WebClient(token=SLCK_API_TOKEN)
    try:
        response = client.chat_postMessage(channel=read_property(
            'slack_api', 'channel'), text=message.as_string())
        assert response["ok"]
        assert response["message"]["text"] == message.as_string()
    except:
        print('ERROR: Please check if the message posted to slack!')


if __name__ == '__main__':
    generate_overall_status()
    convert_to_html_table()
    #print(read_property('sender_credentials', 'sender.email'))
