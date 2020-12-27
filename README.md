## Get in Line: Waiting Times at DMV

The quality of public services matter a lot. If you have to stand in a long line to [pay your electricity bill](https://www.bbc.com/news/world-asia-india-38088385), as was the norm in some third-world countries, it takes away from the time you have to earn money or the time you have for leisure. In this note, we shed light on one aspect of quality for one such public service---waiting times at the DMV.

We scrape data from [CA DMV](https://www.dmv.ca.gov/), which provides average wait times by hour of day for all hours for which a facility is open, to estimate the median average wait time (median of the hourly averages that are reported), variation in wait times by day, hour, and sociodemographics of the local area. 

### Data

#### DMV Data

CA DMV today provides services in a variety of ways: on the phone, the Internet, partner locations, and field offices. Going to the local DMV office is required for only a small set of important services, or if you have trouble using other methods, e.g., the Internet.    

In all, there are 175 DMV field offices in CA. (There are [178 DMV offices](data/yogov_dmv_list.txt) listed on https://yogov.org/dmv/california/california-dmv-locations/. However, three have closed since yogov compiled their list.)

For each DMV field office we collected:

1. **name and location:** "name", "street", "locality", "region", and "zip".
2. **wait time (minutes) by hour:** wait time for the Monday 2pm hour is stored in the column "M14".
3. **services offered:** "title transfers", "licensing services", "replace lost/stolen/damaged", "plates permits & placards", "testing", "records", "registration", "request for miscellaneous original documents."

The final dataset can be downloaded [here](https://github.com/soodoku/wait/blob/master/data/dmv_data_output_12_14_2020.csv). 

To scrape the data, we ran [scripts/get_dmv_wait_data.py](scripts/get_dmv_wait_data.py). The script depends on three pieces of data which we have stored as python lists:
    * [Office Locales](scripts/ca_locales.py)
    * [Services](scripts/services.py)
    * [Output Column Names](scripts/output_columns.py)

#### Sociodemographic Data

We assume that the set of patrons for each DMV office is the set of households for which the DMV office is the closest. Ideally, we want to get the sociodemographic composition of that set of patrons. This requires us to know where each household is located and the sociodemographics of each household. Then, the algorithm for solving it correctly is O(n (households)*DMV offices), which is expensive. We can get some of the data on household location from voter files, property records, etc., but data would be incomplete and we would need to infer variables of interest like income from the property value of the house, which means measurement error. We can solve the problem by choosing a more coarse geographical unit for which census data is available and then solve a problem that finds the closest DMV office for each coarse geographical unit, approximated by its centroid. For our first version, we choose something yet simpler with problems of its own: sociodemographic data of the field office's zip code gotten via the census API. The data we use can be downloaded [here](data/ca_census_data/).

### Analysis and Results

#### Scripts

* [Descriptive Analysis of DMV Wait Time](DMV.ipynb)
* [Correlations Between Wait Time and Sociodemographics](Sociodem.ipynb)

#### Results

The average wait time, averaging over the average for all hours (days). We also estimate the 25th and 75th percentile of wait times for each location.

Next, to assess whether the staffing levels are potentially suboptimal, we estimate average by hour and by weekday, again averaging across locations.

Next, we download town level data on sociodemographics and plot a loess between median income, % African Americans, etc. and the number of services offered, total open time, average wait time, etc. 

### Authors 

Noah Finberg and Gaurav Sood

