# What Exactly Are We Turning Down for Again?

## Summary

Music is part of our daily lives. We listen to it when we work out. We listen to it when we're sad. This project attempts to predict what type of popular music is listened to based on external factors. For instance, if the stock market is up, are the top Billboard hits happy songs? Conversely, if the stock market is down, do people stay indoors and listen to The Cure and Morrissey on repeat?

## Impact:

While there are many examples of machine learning in the music industry, most examples center around recommender systems based on user preferences and associating similar artists. This project instead focuses on using music as an indicator of public sentiment. The sentiment score could be used as general happiness indicator.

A successful score could also be used to aid in the marketing efforts of large music labels. Correlations to outside factors -- such as the stock market -- can inform marketing of new songs.

## Work in space
[50 Years of Pop Music](http://kaylinwalker.com/50-years-of-pop-music/)
[Billboard Volatility](http://decibelsanddecimals.com/dbdblog/2017/1/8/billboard-volatility.html)
[Blue Christmas: A data-driven search for the most depressing Christmas song](https://caitlinhudon.com/2017/12/22/blue-christmas/)
## Next steps:

- Join datasets together
  - Not all songs have unique identifiers
- Create a Song Sentiment score using The Million Song Dataset and the MusixMatch lyrics dataset
- Explore relationship between stock market and Song Sentiment scores
- Define how to define a "Peak" for both scores
- Learn what time series is
- Run Time series model

## Data:

| Source                                                                                    | Description                                                | Format                               | Data Acquired |
|-------------------------------------------------------------------------------------------|------------------------------------------------------------|--------------------------------------|--------------|
| [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset) | Large, detailed dataset of one million songs.              | SQLite DB (summary), HDF5 (detailed) | [Yes](https://github.com/akraemer007/million_song/blob/master/support_files/data_snapshots/msd_data.png)          |
| [MusixMatch Lyrics](https://labrosa.ee.columbia.edu/millionsong/musixmatch)               | Lyrics of 237,622 songs which map to MSD dataset           | SQLite DB (bag of words)             | [Yes](https://github.com/akraemer007/million_song/blob/master/support_files/data_snapshots/lyric_data.png)          |
| [Billboard](http://www.umdmusic.com/default.asp?Lang=English&Chart=D)                     | Billboard Top 20 List going back to 1949                   | CSV                                  | [Yes](https://github.com/akraemer007/million_song/blob/master/support_files/data_snapshots/billboard_data.png)          |
| [S&P 500](https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC)                      | Weekly market highs and lows of S&P 500 going back to 1950 | CSV                                  | [Yes](https://github.com/akraemer007/million_song/blob/master/support_files/data_snapshots/snp500_data.png)          |

## Potential Roadblocks

#### Data issues:

I'm starting with four different data sources. It is possible that joining them may severely limit my dataset. For example, two important datasets -- Billboard and Million Song Dataset -- don't have keys to join them together. I will need to join on track strings. If my data has larger holes than I anticipate, I will pivot from the Million Song Dataset to scraping using the Spotify API.

#### Modeling issues:

I have never created a sentiment score. It is entirely possible I end up making a score that does not reflect reality. If this is the case, I can resort to other other scores that already exist.
Failing to find correlation between the stock market and music sentiment score would be unfortunate.

## Potential Expansions

I am starting with the stock market, but I could expand to other measures. There are several macroeconomic indexes to leverage. Furthermore, there are many big events that happen, which would be interesting to investigate, such as the election and 9/11.
