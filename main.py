import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

def clean_closes(closes):
    closes = closes.replace("Closes:", "")
    closes = closes.replace(" ", "")
    closes = closes.replace("hrs", ":")
    closes = closes.replace("mins", "")
    return closes

def fix_closes(closes):
    if "tomorrow" in closes:
        return(86400)
    if "hrs" in closes:
        closes = clean_closes(closes)
        closes = closes.split(':')
        return ((int(closes[0])*60*60) + (int(closes[1])*60))
    else:
        closes = clean_closes(closes)
        return int(closes)*60
    return(10000)

while True:
    links = []
    URL = "https://www.trademe.co.nz/a/motors/cars/search?odometer_min=100&listed_as=auctions&sort_order=motorsexpiryasc&page=1"
             
    page = requests.get(URL).text
             
    soup = BeautifulSoup(page, 'lxml')
    car = soup.findAll('tg-col', class_ = "l-col l-col--has-flex-contents ng-star-inserted")
    for ca in car:
        link =  ca.find('a')
        links.append("https://www.trademe.co.nz/a/" + link.get('href'))
    
    car_page = requests.get(links[-1]).text
    soup2 = BeautifulSoup(car_page, 'lxml')
    
    time.sleep(8700)
    
    for link in links:
        try:
            car_page = requests.get(link).text
            soup2 = BeautifulSoup(car_page, 'lxml')
            
            carTitle = soup2.find('h1', class_ = "tm-motors-listing__title").text
            location = soup2.find('span', class_ = "tm-motors-date-city-watchlist__location").text
            location = location.replace("Location icon Seller located in ", "")
            reserve = soup2.findAll('p', class_ = "h-text-align-center tm-listing-auction_auction-message--short-message")
            final_bid = soup2.find('p', class_ = "h-text-align-center p-h1").text
            values = soup2.findAll('div', class_ = "tm-motors-vehicle-attributes__tag--content")
            dist_travelled, body, seats, fuel, engine, transmission, col, own_num, imp, wof, reg  = "", "", "", "", "", "", "", "", "", "", ""
        
            for val in values:
                if "Kilometres" in str(val):
                    dist_travelled = val.text
                    dist_travelled = dist_travelled.replace("Kilometres", "")
                elif "Body style" in str(val):
                    body = val.text
                    body = body.replace("Body style", "")
                elif "Seats" in str(val):
                    seats = val.text
                    seats = seats.replace("Seats", "")
                elif "Fuel type" in str(val):
                    fuel = val.text
                    fuel = fuel.replace("Fuel type", "")
                elif "Engine Size" in str(val):
                    engine = val.text
                    engine = engine.replace("Engine Size", "")
                elif "Transmission" in str(val):
                    transmission = val.text
                    transmission = transmission.replace("Transmission", "")
                elif "Exterior colour" in str(val):
                    col = val.text
                    col = col.replace("Exterior colour:", "")
                elif "Number of owners" in str(val):
                    own_num = val.text
                    own_num = own_num.replace("Number of owners:", "")
                elif "Import history" in str(val):
                    imp = val.text
                    imp = imp.replace("Import history", "")
                elif "Registration expires" in str(val):
                    reg = val.text
                    reg = reg.replace("Registration expires:", "")
                elif "WoF expires" in str(val):
                    wof = val.text
                    wof = wof.replace("WoF expires:", "")
        
            with open('car_info2.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                row = [carTitle, location, dist_travelled, body, seats, fuel, engine, transmission, col, own_num, imp, wof, reg, final_bid, reserve[1].text, link]
                writer.writerow(row)
            
            print("Successful", link)
        except:
            print("Failed", link)
