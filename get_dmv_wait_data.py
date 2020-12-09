# First need to get the links for all 2401 DMV field offices in CA - they don't made this easy
# 
# 
# Approach:
# https://www.dmv.ca.gov/portal/locations/ has very restrictive search functionality so it doesn't seem possible just to get a straight up list
# However, one way to get links to all the locations is  to start on one field office and look under "Nearby Wait Times", 
# where there are links to close by field offices.
#

import requests
from bs4 import BeautifulSoup
import csv
import os


# Takes: link to one CA DMV field office page
# Recursively loops through all field office pages
# Writes list of names and links to all CA DMV field office pages to csv
# Returns dictionary of field offices, key: name, value: dmv url
def get_field_offices(start_url, field_offices = {}):
    NUM_FIELD_OFFICES = 2401
    base_url = "https://www.dmv.ca.gov"
    start_page = requests.get(start_url)
    start_soup = BeautifulSoup(start_page.content, 'html.parser')
    
    try:
        #sometimes no nearby offices section on page
        nearby_offices = start_soup.findAll("ul", {"class": "nearby-wait-times"} )[0].findAll("li")
    except:
        return field_offices
    
    for nearby_office in nearby_offices:
        # print(nearby_office.find("a").get("href"))
        name = nearby_office.get_text().split()[0]
        link = base_url + nearby_office.find("a").get("href")

        # print(name)

        if name not in field_offices.keys():
            # write field office to csv
            write_fo_name_and_link_csv(name, link, "fo_list")

            field_offices[name] = link

            # try as new start url
            start_url = link
            print(start_url)
            if len(field_offices) < NUM_FIELD_OFFICES:
                field_offices = get_field_offices(start_url, field_offices)
            else:
                return field_offices

    return field_offices

def write_fo_name_and_link_csv(name, link, file):
    with open(str(file) + ".csv", 'a+', newline='') as csvfile:
        fieldnames = ['name', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'name': name, 'link': link})

# start_page = "https://www.dmv.ca.gov/portal/field-office/woodland/"
start_page = "https://www.dmv.ca.gov/portal/field-office/davis/"
field_offices = get_field_offices(start_page)
# print(field_offices)

# Next go through each field office page and get all the data for wait times, open hours, services provided etc.


# Write to csv