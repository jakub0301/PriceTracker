import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Configuration
URL = 'https://www.amazon.com/dp/B07JP9QJ15/ref=dp_cerb_1'
PRICE = 399.01
YOUR_EMAIL = 'mail@mail.com'
#Gmail account data
USER = 'mail@gmail.com'
PASS = 'pass'


headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'}
page = requests.get(URL, headers=headers)

pretty = BeautifulSoup(page.text,'html.parser').prettify()
soup = BeautifulSoup(pretty,'html.parser')

title = soup.find(id="productTitle").get_text()
print(title.strip())


def check_price():
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:7])
    print(converted_price)

    if(converted_price < PRICE):
        send_mail()
        print("works")
    else:
        print("Still waiting")

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(USER, PASS)
    
    subject = 'Price fell down'
    body = 'Check the amazon link ' + URL
    
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        USER,
        YOUR_EMAIL,
        msg
    )
    print('Email has been sent')
    
    server.quit()

while(True):
    check_price()
    #check every 12 hours
    time.sleep(60 * 60 * 12)

