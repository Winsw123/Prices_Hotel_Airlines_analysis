# Main Goal
Trip: From **TPE, Taiwan** to **HND, Japan**<br>
Duration: 1 years<br>
Target Range: 3-5 star hotels
By comparing the prices of airlines and hotels, we could find high season and the peak travel season

# Target Website
Google travel

# Prices_Hotel_Airlines_analysis
Crawling the info(prices) of hotel and airlines and find its relation

# Tools: Google Selenium and BeautifulSoup
Since the website is dynamic, thus we are going to use Google Selenium and BeautifulSoup to crawl the info and prices

# Steps and Description
## Crawling Steps and Descriptions (Hotels)
At the beginning, we were going to use the "getUrl{level}.py" to get each hotels information(Name, url, star, facilities) output file "output{level}.csv".<br>
Get url is necessary, thus we could locate to the right hotels in the following prices crawling steps.<br>
<br>Then, "prices{level}.py" is going to iterate the "output{level}.csv" crawling the prices and date by each urls respectively.<br>
Output format: "{level}_{index}.csv"

## Crawling Steps and Descriptions (Airlines)
The data format of airlines is simple than the hotels, thus we could easily get the completed data by using the python file "airline.py".


