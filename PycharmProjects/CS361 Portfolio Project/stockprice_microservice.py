import requests
from bs4 import BeautifulSoup
import json
import time

def getStock(ticker):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    url = f'http://finance.yahoo.com/quote/{ticker}'
    r = requests.get(url, headers=headers)
    data = BeautifulSoup(r.text, 'html.parser')
    if data.find('div', {'class':'D(ib) Mend(20px)'}) is not None:
        price = data.find('div', {'class':'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text
        return price
    else:
        return "Error"

def writeFile(f, stock):
    f.seek(0)
    f.write(json.dumps(stock))




if __name__ == '__main__':
    f = open('stockprice.txt', 'r+')
    while True:
        ticker = f.readline()
        if ticker is not None:
            if ticker[0] != "{":
                price = getStock(ticker)
                stock = {'stock':ticker, 'price':price}
                writeFile(f, stock)
        f.seek(0)
        time.sleep(2)