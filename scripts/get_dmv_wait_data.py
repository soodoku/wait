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
import json
import ca_locales, services, output_columns

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# URL FINDER
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# CA_locales = ca_locales.CA_locales
# CA_locales = [l.replace(" ", "-") for l in CA_locales] #format space to dash
# CA_locales = [l.lower() for l in CA_locales] #make all lowercase

# for locale in CA_locales:
#     # check with as many start urls as possible to guess
#     start_url = "https://www.dmv.ca.gov/portal/field-office/" + locale
#     field_offices = get_field_offices(start_url)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# GATHER DMV DATA
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Using fo_full_list.csv, go through each field office page and get all the data for wait times, open hours, services provided etc.
# Data fields - FO Name, Address, wait times, open hours, services provided, payments accepted


# for each field office scrape dmv data
def parse_dmv_fo_page(fo_url):
    dmv_result_dict = {}
    page = requests.get(fo_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    dmv_data = soup.find("script", { "id": "single-location-map-js-extra"})
    dmv_data = str(dmv_data).split("*/")[1].split("/*")[0].replace("var dmvLocation = ", "").replace(";", "")
    
    # get wait times per day and hour
    wait_times_dict = parse_wait_times(dmv_data)
    # print(wait_times_dict)
    
    # add additional dmv info
    dmv_data_dict = parse_dmv_specific_data(soup)
    # print(dmv_data_dict)

    # Services Provided
    services_dict = parse_services(soup)
    
    dmv_result_dict = dict(dmv_data_dict)
    dmv_result_dict.update(wait_times_dict)
    dmv_result_dict.update(services_dict)
    return dmv_result_dict


# takes json string of wait time data and returns a dictionary correponding to wait times at the dmv
def parse_wait_times(dmv_data):
    json_data = json.loads(dmv_data)
    json_wait_times = json_data["wait_times"]
    # print(json_wait_times)

    # update wait_times_dict
    wait_times_dict = initialize_wait_times_dict()
    for key, values_dict in json_wait_times.items():
        # print(key, '->', dict(values_dict))
        for hour, wait_time in dict(values_dict).items():
            # print(key)
            # print(int(hour))
            # print(wait_time)
            if key == "Sunday":   
                label = "SU" + str(int(hour))
            elif key == "Monday":
                label = "M" + str(int(hour))
            elif key == "Tuesday":
                label = "TU" + str(int(hour))
            elif key == "Wednesday":
                label = "W" + str(int(hour))
            elif key == "Thursday":
                label = "TH" + str(int(hour))
            elif key == "Friday":
                label = "F" + str(int(hour))
            elif key == "Saturday":
                label = "SA" + str(int(hour))
            else:
                continue
            # print("adding hour: {} with wait time of: {} ".format(label, wait_time))
            wait_times_dict[label] = wait_time

    return wait_times_dict

def parse_dmv_specific_data(soup):
    dmv_data_dict = {}
    # FO NAME
    fo_name = soup.title.get_text().split("-")[0].rstrip()
    
    # Address
    # <span itemprop="streetAddress">1711 East Main Street</span>
    fo_street_address = soup.find("span", itemprop="streetAddress").get_text()

    # <span itemprop="addressLocality">, Visalia,</span>
    fo_locality = soup.find("span", itemprop="addressLocality").get_text().replace(",", "").rstrip()
    
    # <span itemprop="addressRegion"> CA</span> (probably all CA, but I'll get this field anyway)
    fo_region = soup.find("span", itemprop="addressRegion").get_text()

    # <span itemprop="postalCode">93292</span>
    fo_zip = soup.find("span", itemprop="postalCode").get_text()

    # print("address: {} - {} - {} - {}".format(fo_street_address, fo_locality, fo_region, fo_zip))
    dmv_data_dict["name"] = fo_name
    dmv_data_dict["street"] = fo_street_address
    dmv_data_dict["locality"] = fo_locality
    dmv_data_dict["region"] = fo_region
    dmv_data_dict["zip"] = fo_zip
 
    return dmv_data_dict

def parse_services(soup):
    services_dict = initialize_services_dict()
    services = soup.findAll("ul", {"class": "location-services-list"} )[0].findAll("li")
    for service in services:
        s = service.get_text().lower().rstrip().replace(",", "")
        services_dict[s] = 1
    return services_dict
# sets up up an empty dictionary corresponding to every day and every hour
# wait_times_dict will store wait times with a key of DayHour(military time), value: (wait time in minutes)
# e.g. SU0: NA....corresponding to Sunday at midnight with no value (DMV closed) and M8: 10...corresponding to Monday at 8 am with a 10 minute wait.
# will likely be many columns where no dmv location is open (e.g. 2am), but I will track every hour and we can eliminate those columns if we'd like to later
def initialize_wait_times_dict():
    days_of_week = ["SU", "M", "TU", "W", "TH", "F", "SA"]
    hours_in_day = [i for i in range(24)]
    wait_times_dict = {}

    for day in days_of_week:
        for hour in hours_in_day:
            key = day + str(hour)
            wait_times_dict[key] = "NA"
    
    return wait_times_dict

def initialize_services_dict():
    services_dict = {}
    dmv_services = [i.lower().rstrip() for i in services.DMV_SERVICES]
    for service in dmv_services:
        services_dict[service] = "NA"
    return services_dict


csv_file = "../data/dmv_data_output_12_14_2020.csv" #output file

# read fo_full_list.csv to list
with open('../data/fo_full_list.csv', newline='') as f:
    dmv_list = [row[0] for row in csv.reader(f)] 

# print(wait_times_dict)

for fo_url in dmv_list:
    print("scraping: {}".format(fo_url))
    dmv_result_dict = parse_dmv_fo_page(fo_url)
    # write dmv data to csv
    with open(csv_file, 'a+', newline='') as csvfile:
        fieldnames = output_columns.OUTPUT_COLUMN_NAMES
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(dmv_result_dict)