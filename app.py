import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json
import requests
from datetime import datetime
from urllib.parse import quote
import pytz




vfs_email = os.environ.get('VFS_USER_EAMIL')
vfs_password = os.environ.get('VFS_PASSWORD')
# I just implemented gmail
gmail_sender = "your@gmail.com"
email_receiver = ["a@email.com", "b@email.com"]
#Get your gmail app password from here https://myaccount.google.com/apppasswords
gmail_password = os.environ.get('GMAIL_PWD')

#for the query, the center code you can fine here
#https://lift-apicn.vfsglobal.com/master/center/deu/chn/zh-CN
center = "GRCG"


berlin_timezone = pytz.timezone('Europe/Berlin')
now = datetime.now(berlin_timezone)
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def newLogin():
    url = "https://lift-apicn.vfsglobal.com/user/login"
    payload = {
        'username': vfs_email,
        'password': vfs_password,
        'missioncode': 'deu',
        'countrycode':'chn'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == requests.codes.ok:
        # Extract the access token value from the response JSON
        response_json = json.loads(response.text)
        if response_json['error'] != None :
            raise Exception(f'Error: {response_json["error"]["code"]} - {response_json["error"]["description"]}')
        access_token = response_json['accessToken']
        print("access_token  " + access_token)
        return access_token
    else:
        raise Exception(f'Error: {response.status_code} - {response.text}')
def getTime(token):
    encoded_email = quote(vfs_email)
    startDate = quote(dt_string[:10], safe='')
    url = f"https://lift-apicn.vfsglobal.com/appointment/slots?countryCode=chn&missionCode=deu&centerCode={center}G&loginUser={encoded_email}&visaCategoryCode=SV&languageCode=zh-CN&applicantsCount=1&days=180&fromDate={startDate}&slotType=2"
    headers['Authorization'] = token
    response = requests.get(url, headers=headers)

    if response.status_code == requests.codes.ok:
        # Extract the access token value from the response JSON
        response_json = json.loads(response.text)
        new_time = response_json[0]['date']
        return new_time
    else:
        raise Exception(f'Error: {response.status_code} - {response.text}')
def sendEmail(new_time):

    message = MIMEMultipart()
    message['From'] = gmail_sender
    message['To'] = ', '.join(email_receiver)
    message['Subject'] = f'new time available  {new_time}'

    # Add the body of the email
    body = f'new VFS Termin  {new_time}'
    message.attach(MIMEText(body, 'plain'))

    # Connect to the Gmail SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(gmail_sender, gmail_password)

        # Send the email
        smtp.sendmail(gmail_sender, email_receiver, message.as_string())
    print("Email sent")

if vfs_password is None or gmail_password is None or len(vfs_password) < 1 or len(gmail_password) < 1:
    raise Exception("No password")

token = newLogin()
new_time = getTime(token)
sendEmail(new_time)
print(f"Time: {new_time}")



