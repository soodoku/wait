## Wait

We scrape data from [CA DMV](https://www.dmv.ca.gov/portal/field-office/woodland/) to answer whether the number of services, the average wait time, the hours a facility is open, etc. vary by income.
 
## Data
 
It looks like there are approximately 163 DMV field offices in CA (scraper wasn't able to find any more). This number does however seem to be backed up elsewhere. https://yogov.org/dmv/california/california-dmv-locations/ estimates ~180 field offices. It's possible I've missed a couple in scraping. Will think through how I might determine if this is the case.

## Analysis

We estimate the average wait time, averaging over the average for all hours (days). We also estimate the 25th and 75th percentile of wait times for each location.

Next, to assess whether the staffing levels are potentially suboptimal, we estimate average by hour and by weekday, again averaging across locations.

Next, we download town level data on sociodemographics and plot a loess between median income, % African Americans, etc. and the number of services offered, total open time, average wait time, etc. 

## Authors 

Noah Finberg and Gaurav Sood

