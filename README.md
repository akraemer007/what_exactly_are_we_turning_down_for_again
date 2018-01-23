# What Exactly Are We Turning Down for Again?
__Abstract:__ This project is an analysis of happiness in music and the external factors that drive it. 
__Hypothesis:__ Music is a representation of our mood. Therefore when the national mood is high, people listen to happy music.
__Results:__ Using logistic regression, I discovered a negative relationship between the consumer confidence index and when the No. 1 billboard hit is a happy song. I found that people are especially likely to listen to happy music following a national tragedy.

See this work as a presentation in [slide format].

[See the video].

# Background & Motivation
Music is part of our daily lives. We listen to it when we work out. We listen to it when we're sad. This project attempts to predict what type of popular music is listened to based on external factors. For instance, if the Consumer Confidence Index is up, are the top Billboard hits happy songs? Conversely, if the Consumer Confidence Index is down, do people stay indoors and listen to The Cure and Morrissey on repeat?

Also, why on earth was *[The Macarena]* the No. 1 Billboard hit for 14 straight weeks in 1996?

# Data used

| Source                                                                                                    | Description                               | Format                                                                        |
|-----------------------------------------------------------------------------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------|
| [Billboard](https://github.com/dbfowler/billboard_volatility/blob/master/Raw%20Data/all_charts.csv)       | Billboard Top 100 List going back to 1958 | CSV                                                                           |
| [Consumer Confidence Index](https://data.oecd.org/leadind/consumer-confidence-index-cci.htm)              | Monthly Index value going back to 1960    | CSV                                                                           |
| [Spotify API](https://developer.spotify.com/web-api/)                                                     | Song valence and energy scores            | [API](https://github.com/charlie86/spotifyr)                                  |
| [MetroLyrics](www.metrolyrics.com/), [songlyrics](www.songlyrics.com/), [lyricsmode](www.lyricsmode.com/) | Lyrics billboard hits                     | [Scraped](https://github.com/walkerkq/musiclyrics/blob/master/01_songscrape.R)|


# Analysis methods
<img src="images/workflow.png" height=80%, width=80%, alt=“Project_Pipeline”>

# Predicting malware events
# Future improvements
# Acknowledgements
Thank you to the following data scientists for inspiration for the project.
[50 Years of Pop Music]
[Billboard Volatility]
[Blue Christmas: A data-driven search for the most depressing Christmas song]

