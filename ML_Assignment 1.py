#!/usr/bin/env python
# coding: utf-8

# author : mirza_inayat

import requests
from bs4 import BeautifulSoup
import pandas as pd

'''html = """<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>

</body>
</html>"""

soup = BeautifulSoup(html, 'html.parser')

hotel_card = [100]'''

def set_url(city_name):
    base_url = 'https://www.goibibo.com/hotels/hotels-in-' + city_name + '-ct/'
    return base_url

def webscrap(city_name):
    page = requests.get(set_url(city_name))
    global soup
    soup = BeautifulSoup(page.content, 'html.parser')
    global hotel_card
    hotel_card = soup.find_all(class_ = 'HotelCardstyles__WrapperSectionMetaDiv-sc-1s80tyk-2 fKNNeH')

def get_names():
    hotel_names_tags = soup.select(" .HotelCardstyles__HotelNameWrapperDiv-sc-1s80tyk-11.jkwhbV ") 
    names = [hn.a['content'] for hn in hotel_names_tags]
    #names = [hn.find('a').get('content') for hn in hotel_names_tags]
    #print(len(names))
    return names

def get_address():
    address_tags = soup.select('.HotelCardstyles__HeadingInfoWrapperDiv-sc-1s80tyk-9.ynTNd')
    addresses = [at.find(itemprop = 'address').get_text() for at in address_tags]
    #print(len(addresses))
    return addresses

def get_description():
    roomdescrip = []
    for i in range(len(get_names())):
        roomds_tags = hotel_card[i].select('.HotelCardstyles__RoomTypeTextWrapper-sc-1s80tyk-14')
        roomd = [rd.get_text() for rd in roomds_tags]
        roomdescrip.append(roomd)
        #print(roomdescrip[i])
    return roomdescrip

def get_amenities():
    all_amenities = []
    for i in range(len(get_names())):
        amenities_tags = hotel_card[i].select('.AmenitiesListstyles__TextWrapper-sc-19dqtu1-7.kQzGvm')
        allam = [aa.get_text() for aa in amenities_tags]
        all_amenities.append(allam)
        #print(len(all_amenities[i]))
        #print(all_amenities[i])
    return all_amenities

def get_facilities():
    other_facilities = []
    for i in range(len(get_names())):
        other_facilities_tags = hotel_card[i].select('.PersuasionHoverTextstyles__TextWrapperSpan-sc-1c06rw1-14.bsmZUs')
        other_fac = [fc.get_text() for fc in other_facilities_tags]
        other_facilities.append(other_fac)
        #print(len(other_facilities[i]))
        #print(other_facilities[i])
    return other_facilities

def get_price():
    price_tags = soup.select('.HotelCardstyles__CurrentPriceTextWrapper-sc-1s80tyk-25.lnAxKT')
    prices = [pr.get_text() for pr in price_tags]
    #print(len(prices))
    return prices

def get_offers():
    offer_tags = soup.select('.PersuasionHoverTextstyles__TextWrapperSpan-sc-1c06rw1-14.eYCzxX')
    offers = [of.get_text() for of in offer_tags]
    #print(len(offers))
    return offers

def construct_df(city_name):
    webscrap(city_name)
    ctarr = []
    for i in range(len(get_names())):
        ctarr.append(city_name) 

    Hotels = pd.DataFrame({
        'Name' : get_names(),
        'Address' : get_address(),
        'Description' : get_description(),
        'Facility' : get_facilities(),
        'Amenities' : get_amenities(),
        'Offers' : get_offers(),
        'Price per Room' : get_price(),
        'City' : ctarr
    })
#    Hotels = pd.DataFrame(Hs)
#    Hotels.transpose()
    return Hotels

'''
df = pd.DataFrame.from_dict(a, orient='index')

df.transpose()

df.to_csv('website3.csv', index=False,header=True, encoding='utf-8')
'''
Cities = ['delhi','jaipur','udaipur']

#for city in Cities:
#    construct_df(city).to_csv(city + '.csv')

df0 = construct_df('delhi')
df1 = construct_df('jaipur') 
df2 = construct_df('udaipur')

frames = [df0,df1,df2]
dfinal = pd.concat(frames)
dfinal.to_csv('ML1.csv')

#webscrap('delhi')
#print soup
#print get_names()

#extract data of new city
#construct_df('jaipur').to_csv('ML2.csv')
