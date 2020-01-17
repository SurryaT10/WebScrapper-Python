from bs4 import BeautifulSoup
import requests
import smtplib
import time


def checkPrice():

    # USE 'httpbin.org' for authentication purpose
    
    URL = 'https://www.amazon.in/adidas-Backpack-Messi-Kids-Bp/dp/B0794X714M/ref=sr_1_12?keywords=adidas+bags&qid=1578149366&sr=8-12'    #Amazon link
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    
    page = requests.get(URL, headers=headers)                                   #gets the page from the URL

    soup = BeautifulSoup(page.text, 'html.parser')                              #parses the url into html format

    priceString = soup.find(id='priceblock_saleprice').get_text()               #finds html element with id='priceblock_saleprice'

    originalPrice = priceString[2:3]
    originalPrice += priceString[4:]
    originalPrice = float(originalPrice)                                       

    print("Price of the Bag is : ",originalPrice)

    if originalPrice < 3000:                                                    #sends mail if cost < 3000
        sendMail()

def sendMail():
    server = smtplib.SMTP('smtp.gmail.com', 587)                                #handles email requests
    server.ehlo()                                                               #protocol to communicate between both servers
    server.starttls()                                                           
    server.ehlo()

    server.login('yourmail@gmail.com', '2-step-verification-App Password-for Window/IOS Computer')                   #login credentials - Your details

    subject = 'Price fell down!'
    body = 'Check the amazon link https://www.amazon.in/adidas-Backpack-Messi-Kids-Bp/dp/B0794X714M/ref=sr_1_12?keywords=adidas+bags&qid=1578149366&sr=8-12'

    msg = f"Subject:{subject} \n\n {body}"

    server.sendmail(
        'from-mail.gmail.com',
        'to-mail@gmail.com',
        msg
    )

    print("Mail has been sent!")
    server.quit()

while(True):
    checkPrice()
    print("done")
    time.sleep(60*60*24)