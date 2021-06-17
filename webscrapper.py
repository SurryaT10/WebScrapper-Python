from bs4 import BeautifulSoup
import requests
import smtplib
import time
from decouple import config

#URL = 'https://www.amazon.in/adidas-Backpack-Messi-Kids-Bp/dp/B0794X714M/ref=sr_1_12?keywords=adidas+bags&qid=1578149366&sr=8-12'    #Amazon link
URL = 'https://www.flipkart.com/adidas-finale-cdf-comp-football-size-5/p/itmaf6ac85f891aa?pid=BALFGHY8GJYY59QN&lid=LSTBALFGHY8GJYY59QNGRZ7C6&marketplace=FLIPKART&q=adidas+finale&store=search.flipkart.com&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=785ab3cb-2eec-4a97-a370-6c2a43b19442.BALFGHY8GJYY59QN.SEARCH&ppt=sp&ppn=sp&ssid=wmlxa315fk0000001623946032458&qH=f7727e914e7d8c25'
EMAIL = config('EMAIL_ID')
SECURITY_KEY = config('SECURITY_KEY')

def checkPrice():

    # USE 'httpbin.org' for authentication purpose
    
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    
    page = requests.get(URL, headers=headers)                                   #gets the page from the URL

    soup = BeautifulSoup(page.text, 'html.parser')                              #parses the url into html format

    priceString = soup.find("div", class_="_3I9_wc _2p6lqe").get_text()               #finds html element with id='priceblock_saleprice'

    originalPrice = ''.join(e for e in priceString if e.isalnum())
    originalPrice = float(originalPrice)                                      

    print("Price of the Bag is : ",priceString)

    if originalPrice < 10000:                                                    #sends mail if cost < 3000
        sendMail()

def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)                                #handles email requests
    server.ehlo()                                                               #protocol to communicate between both servers
    server.starttls()                                                           
    server.ehlo()

    server.login(EMAIL, SECURITY_KEY)                   #login credentials - Your details

    subject = 'Price fell down!'
    body = 'Check the amazon link ' + URL

    msg = f"Subject:{subject} \n\n {body}"

    server.sendmail(
        EMAIL,
        EMAIL,
        msg
    )

    print("Mail has been sent!")
    server.quit()

while(True):
    checkPrice()
    print("done")
    time.sleep(60*60*24)