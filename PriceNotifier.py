import requests
import smtplib
from bs4 import BeautifulSoup
from decouple import config

#URL = 'https://www.amazon.in/ASUS-i7-10750H-Graphics-Original-G712LU-H7015T/dp/B08DVLCNKK/ref=sr_1_4?crid=LIH9CVBYDTSN&dchild=1'
# Need to set the user-agent(google search my user-agent)

headers = {
    'User-Agent': config('USER_AGENT')}  # Price Checker


def check_price(URL, headers, target):
    # Get the page
    page = requests.get(URL, headers=headers)
    # Get the required tags via inspecting the element
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text().strip()
    # Fromatting the data
    currency = price[0:2]
    price = price[2:price.index('.')]
    price = price.replace(',', '')
    price = int(price)
    if(price < target):
        send_mail()
    print(f'Product Title : {title} \n Product Price : {price} {currency}')


def send_mail():
    # SMTP Setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # App passwords for account enabled after 2FA
    server.login(sender, config('APP_PASS'))
    subject = 'Price dop'
    body = 'Check the amazon link '+URL + \
        '\n This is an autogenerated email by Abdulaziz using WebScraping in Python'
    msg = f'{subject}\n\n {body}\n'
    server.sendmail(sender, receiver, msg)
    print('Email sent successfully')
    server.quit()


# MAIN_PROGRAM
# You can run this code in an infinite loop and use time.sleep(time)
URL = input('Enter the URL of your amazon product : \n')
target = int(input('Enter your target price : '))
try:
    sender = config('SENDER')
except:
    sender = input(
        'Enter sender Email address(2FA must be enabled) : \n')
try:
    receiver = config('RECEIVER')
except:
    receiver = input(
        'Enter receiving email address : \n')
check_price(URL, headers, target=100000)
