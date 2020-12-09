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


# Takes: link to one CA DMV field office page
# Returns: list of dictionary of links to all CA DMV field office pages. Key: FO name, Value: link
def get_field_offices(start_url):
    field_offices = {}
    base_url = "https://www.dmv.ca.gov"
    start_page = requests.get(start_url)
    start_soup = BeautifulSoup(start_page.content, 'html.parser')
    
    nearby_offices = start_soup.findAll("ul", {"class": "nearby-wait-times"} ).findAll("li")
    print(nearby_offices)
    # nearby_offices_names =
    # nearby_offices_links =
    # for nearby_office in nearby_offices:
    #     print(nearby_office.find("a").get("href"))
    #     name = nearby_office.get_text().split()[0]
    #     link = base_url + nearby_office.find("a").get("href")
    #     # print("NAME: {}".format(name))
    #     # print("LINK: {}".format(link))

    #     if name not in field_offices.keys():
    #         field_offices[name] = link

    print(field_offices)

start_page = "https://www.dmv.ca.gov/portal/field-office/woodland/"
get_field_offices(start_page)

# Next go through each field office page and get all the data for wait times, open hours, services provided etc.


# Write to csv