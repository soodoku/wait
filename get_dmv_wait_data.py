# First need to get the links for all 2401 DMV field offices in CA - they don't made this easy
# 
# 
# Approach:
# https://www.dmv.ca.gov/portal/locations/ has very restrictive search functionality so it doesn't seem possible just to get a straight up list
# However, one way to get links to all the locations is  to start on one field office and look under "Nearby Wait Times", 
# where there are links to close by field offices.
#
# note: in order to get all the field offices, need to run the function multiple times from starting points across different parts of the state...
# can get stuck in a loop (ie. sometimes only shows same nearby offices)

import requests
from bs4 import BeautifulSoup
import csv
import os
from ca_locales import CA_locales #list of ca locations



# Takes: link to one CA DMV field office page
# Recursively loops through all field office pages
# Writes list of names and links to all CA DMV field office pages to csv
# Returns list of field office urls
def get_field_offices(start_url, field_offices = []):
    NUM_FIELD_OFFICES = 2401
    base_url = "https://www.dmv.ca.gov"
    start_page = requests.get(start_url)

    if start_page.status_code != 200:
        return field_offices

    start_soup = BeautifulSoup(start_page.content, 'html.parser')
    
    try:
        #sometimes no nearby offices section on page
        nearby_offices = start_soup.findAll("ul", {"class": "nearby-wait-times"} )[0].findAll("li")
    except:
        return field_offices
    
    for nearby_office in nearby_offices:
        # print(nearby_office.find("a").get("href"))
        link = base_url + nearby_office.find("a").get("href")

        # print(name)

        if link not in field_offices:
            # write field office to csv
            write_fo_name_and_link_csv(link, "fo_full_list")

            field_offices.append(link)

            # try as new start url
            start_url = link
            print(start_url)
            if len(field_offices) < NUM_FIELD_OFFICES:
                field_offices = get_field_offices(start_url, field_offices)
            else:
                return field_offices

    return field_offices

def write_fo_name_and_link_csv(link, file):
    with open(str(file) + ".csv", 'a+', newline='') as csvfile:
        fieldnames = ['link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'link': link})


CA_locales = [l.replace(" ", "-") for l in CA_locales] #format space to dash
CA_locales = [l.lower() for l in CA_locales] #make all lowercase

for locale in CA_locales:
    # check with as many start urls as possible to guess
    start_url = "https://www.dmv.ca.gov/portal/field-office/" + locale
    field_offices = get_field_offices(start_url)




# Next go through each field office page and get all the data for wait times, open hours, services provided etc.


# Write to csv