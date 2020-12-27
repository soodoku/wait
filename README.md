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

**Note** CA DMV does not report over how long a period it averages the wait time. 

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

CA DMV on the whole seems to be doing an excellent job. The median wait time (median of the hourly buckets) across facilities is around 12 minutes. There are, however, a few field offices, e.g., Hollywood and Temecula, where the median wait time is over 40 minutes.

![Median Wait Times](figs/dmv_average_wait_by_field_office.png)

Yet more reassuringly, the 75th percentile of the wait times is about 20 minutes. The 75th percentile of the 75th percentile is just over 30 minutes. But once again there are a few offices where the numbers look alarming. For instance, in Temecula, the 75th percentile is nearly 70 minutes.

![75th Percentile Wait Times](figs/dmv_75_percentile_wait_by_field_office.png)

Plotting the 25th percentile provides a different view. The median of the 25th percentile is around 2 minutes. This suggests that the offices are likely overstaffed for 25% of the hours as a 2 minute turnaround time means that many people are getting served as soon as they get in, which suggests that some of the officials are likely waiting while people pour in. The short turnaround times could be explained by advanced reservations but you have to pair the data above to get at what percentage of people are likely using the advanced reservation system. (There is of course the possibility that people who use advanced reservation system book during certain times more often.) The larger question is about staffing and about what the optimal staffing levels should look like if say the objective was to reduce wait time given fixed resources (and then plausibly expand it in a way that prices people's time appropriately so that we are increasing welfare. A [recent paper](http://s3.amazonaws.com/fieldexperiments-papers2/papers/00720.pdf) suggests Value of Time at about $19/hr with variation across cities.)

![25th Percentile Wait Times](figs/dmv_25_percentile_wait_by_field_office.png)

The average wait time, averaging over the average for all hours (days). We also estimate the 25th and 75th percentile of wait times for each location.

Next, to assess whether the staffing levels are potentially suboptimal, we estimate average by hour and by weekday, again averaging across locations.

Next, we download town level data on sociodemographics and plot a loess between median income, % African Americans, etc. and the number of services offered, total open time, average wait time, etc. 

### Authors 

Noah Finberg and Gaurav Sood

