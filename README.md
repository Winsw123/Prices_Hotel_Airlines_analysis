# Final Report (Chinese)
Detailed report and full record of results in the folder "report_and_ppt".<br>
[GitHub] (https://www.youtube.com/watch?v=FA9FYOnWbPc)

# Main Goal
Trip: From **TPE, Taiwan** to **HND, Japan**<br>
Duration: 1 year<br>
Target Range: 3-5 star hotels
By comparing the prices of airfare and hotels, we could find high season and the peak travel season

# Brief introduction of the problem
In modern people's busy lives, they often want to travel to other countries during their free time. When traveling, price is an important factor to consider. Various factors can cause hotel prices to fluctuate, such as flight discounts, labor costs, and local living expenses.<br><br> 

We believe that airfare prices are a key factor influencing hotel prices. By analyzing the relationship between hotel prices and airfare prices, we aim to determine their correlation. If a connection exists, consumers can use the current airfare prices to estimate whether the current hotel prices are reasonable, helping them decide whether to book a particular hotel.

# Target Website
Google travel

# Prices_Hotel_Airlines_analysis
Crawling the info(prices) of hotel and airfare and find its relation

# Tools: Google Selenium and BeautifulSoup
Since the website is dynamic, thus we are going to use Google Selenium and BeautifulSoup to crawl the info and prices

# Data Integration and Preprocessing
## Crawling Steps and Descriptions (Hotels)
At the beginning, we were going to use the "getUrl{level}.py" to get each hotels information(Name, url, star, facilities) output file "output{level}.csv".<br>
Get url is necessary, thus we could locate to the right hotels in the following prices crawling steps.<br>
<br>Then, "prices{level}.py" is going to iterate the "output{level}.csv" crawling the prices and date by each urls respectively.<br>
Output format: "{level}_{index}.csv"

## Crawling Steps and Descriptions (Airfare)
We were going to crawl the economy airlines data to get the most economical prices (one-way).<br>
The main reason is that its price trend fluctuations are easier to identify.

## Data preprocessing
We first preprocess the hotel price data, handling different star ratings separately. The method used here involves initially plotting line charts to observe the price trends of all hotels and removing hotels with abnormal price patterns.<br>

<br>Since each hotel has a different price range, we standardize the price range for each hotel and then calculate the average to analyze the overall trend. This results in three averaged datasets (for 3-star, 4-star, and 5-star hotels), which we then compare with airfare prices.<br>

<br>For the analysis, we use correlation analysis, Granger causality test (to evaluate whether the historical values of one variable can be used to predict another), and visualization charts for intuitive comparison.<br>

After conducting the analysis, we found that the overall scores and results were not satisfactory, and there was no clear pattern between airfare prices and hotel prices that could be identified visually.




