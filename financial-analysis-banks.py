#%% md

# Finance Data Project | Bank Stocks Analysis, 2006-2016, Bank Financial Crisis
# BY: Sumit Chaurasia, ML/AI Engineer and Developer

# Some part of this Project is based on analysis on financial crisis of 2008-2009 for different banks. The Bank datasets has been imported from pandas library. It is just a visualising project and not a robust project.
____

# We'll focus on bank stocks and see how they progressed throughout the [financial crisis](https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%9308) all the way to early 2016.

#%% md

## Get the Data

# I used pandas to directly read data from Google finance using pandas!
#
# First we need to start with the proper imports
#
# *Note: [You'll need to install pandas-datareader for this to work!](https://github.com/pydata/pandas-datareader) Pandas datareader allows you to [read stock information directly from the internet](http://pandas.pydata.org/pandas-docs/stable/remote_data.html) Use these links for install guidance (**pip install pandas-datareader**), or just follow along with the video lecture.*

### The Imports

#%%

from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
%matplotlib inline

#%% md

## Data

We need to get data using pandas datareader. We will get stock information for the following banks:
    *  Bank of America
               * CitiGroup
               * Goldman Sachs
                         * JPMorgan Chase
                                    * Morgan Stanley
                                             * Wells Fargo

                                                     **get the stock data from Jan 1st 2006 to Jan 1st 2016 for each of these banks. Set each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol. This will involve a few steps:**
1. Use datetime to set start and end datetime objects.
2. Figure out the ticker symbol for each bank.
2. Figure out how to use datareader to grab info on the stock.

# Bank of America
BAC = data.DataReader("BAC", 'google', start, end)


#%%

start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)

#%%

BAC = data.DataReader('BAC','yahoo',start,end)
#for citibank

C = data.DataReader("C", 'yahoo', start, end)

#for goldman sachs
GS = data.DataReader("GS", 'yahoo', start, end)

#for JPMC
JPM = data.DataReader("JPM", 'yahoo', start, end)

#for Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)

#for Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

#%%

MS

#%%

GS

#%% md

** Create a list of the ticker symbols (as strings) in alphabetical order. Let's Call this list: tickers**

#%%

tickers = ['BAC', 'C', 'GS', 'JPM','MS','WFC']

#%% md

**Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks. Set the keys argument equal to the tickers list. Creating on column.**

#%%

bank_stocks = pd.concat([BAC,C,GS,MS,JPM,WFC], axis = 1, keys = tickers)

#%%

bank_stocks.head()

#%% md

**Let's set the column name:**

#%%

bank_stocks.columns.names = ['Bank Ticker','Stock Info']

#%% md

**Check the head of the bank_stocks dataframe.**

#%%

bank_stocks.head()

#%% md

# Exploratory Data Analysis

Let's explore the data a bit! Before continuing, I encourage you to check out the documentation on [Multi-Level Indexing](http://pandas.pydata.org/pandas-docs/stable/advanced.html) and [Using .xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html).

**The max Close price for each bank's stock throughout the time period is analysed here in this section**

#%%

#One way to check maximum close price
# for tick in tickers:
#     print(tick,bank_stocks[tick]['Close'].max())

# Another method
bank_stocks.xs(key='Close', axis=1, level='Stock Info').max()

#%% md

** Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:** price p at time t

$$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

#%%

returns = pd.DataFrame()

#%% md

** We can use pandas pct_change() method on the Close column to create a column representing this return value. Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.**

#%%

for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()

#%%

returns.head()

#%% md

**Create a pairplot using seaborn of the returns dataframe.Analyse Data**

#%%

sns.pairplot(returns[1:])

#%% md

* CITIGROUP had a crash on November 2008, but according to plots, JPM returns were in danger and financial crisis actually affected JPMC too. [Yahoo dataset report]

* We also see MS in Financial crisis problems as the plot refers



#%% md

**Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns. We noticed that 4 of the banks share the same day for the worst drop, did anything significant happen that day, let's see that**

#%%

# Worst Drop (4 of them on Inauguration day)
returns.idxmin()

#%% md

**We noticed that MS's and JPMC largest drop and biggest gain were very close to one another**
BUT, CITIGROUP had a stock split in May 2011. In google datasets, things were different
NOTE: when using google dataset, I noticed CITI had a stock split as it's largest drop and biggest gain were very close

#%%

# Best Single Day Gain
# citigroup stock split in May 2011, but also JPM day after inauguration.
returns.idxmax()

#%% md

**Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

#%%

returns.std() # GS and MS riskiest, according to yahoo dataset, but actually CITI was riskiest

#%%

returns.loc['2015-01-01':'2015-12-31'].std()  #we see similar risk profiles for all banks, but for BAC and JPM. WFC had lowest

#%% md

**Create a distplot using seaborn of the 2015 returns for Morgan Stanley**

#%%

sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=50)

#%% md

**Create a distplot using seaborn of the 2008 returns for CitiGroup** This gives us an accurate visualisation about CITIGROUP financial crisis

#%%

sns.distplot(returns.loc['2008-01-01':'2008-12-31']['C Return'],color='red',bins=100)

#%% md

____
# More Visualization

A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.

### Imports

#%%

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
%matplotlib inline

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()

#%% md

**Create a line plot showing Close price for each bank for the entire index of time.**

#%%

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()

#%% md

**Well, now it is more clear that CITIGROUP had a financial crisis and it is visible on our plot. That Was Great Recession.**

#%%

bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()

#%%

# plotly, notebook validations fail here, check stackoverflow for solution of error
bank_stocks.xs(key='Close',axis=1,level='Stock Info').iplot()

#%% md

## Moving Averages

Let's analyze the moving averages for these stocks in the year 2008.

**Plotting the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

#%%

plt.figure(figsize=(12,6))
BAC['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].loc['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()

#%% md

**Create a heatmap of the correlation between the stocks Close Price.**

#%%

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

#%% md

**Just a show: Use seaborn's clustermap to cluster the correlations together:**

#%%

sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

#%% md

# That's the end of analysis. We figured out various insights regarding financial crisis, 2006-2016

# Some Insights that were important:
# 1. CITIBANK had financial crisis, that was the biggest Recession period on Nov 2011
# 2. Morgan Stanley and JPMC were also hugely affected
# 3. The largest drop and biggest gain of CITIBANK was happened during 2011 when CITIGROUP actually announced Stock Splits. Even MS and JPMC were affected
