import pandas as pd
import numpy as np


chart_df = pd.read_csv('../data/all_charts.csv')
chart_df = chart_df[['chartDate',
                     'title',
                     'artist',
                     'peakPos',
                     'lastPos',
                     'weeks',
                     'rank',
                     'change',
                     'spotifyID']]
chart_df['chartDate'] = pd.to_datetime(chart_df[('chartDate')])
chart_df['year'] = chart_df['chartDate'].dt.year
chart_df['month'] = chart_df['chartDate'].dt.month
chart_df['decade'] = (chart_df.chartDate.dt.year//10)*10
chart_df['rank_weight'] = 101 - chart_df['rank']

# Only keep top 10
chart_df = chart_df[chart_df['rank'] < 11]


### SPOTIFY DATA ###
spotify_df = pd.read_csv('../data/spotify_data.csv')
spotify_df = spotify_df.drop_duplicates() # remove one spotify dup
spotify_df['maj_minor'] = spotify_df['key_mode'].str.split(' ', 1).str[1]


### LYRICS DATA ###
lyrics_df = pd.read_csv('../data/lyrics.csv')
lyrics_df = lyrics_df[lyrics_df['Source'].notnull()] # remove songs without lyrics

# Create TextBlob object. Extract polarity score
from textblob import TextBlob
lyrics_df['tb_obj'] = lyrics_df['Lyrics'].apply(lambda lyric: TextBlob(lyric)) # takes a bit to run
lyrics_df['polarity'] = lyrics_df['tb_obj'].apply(lambda tb_obj: tb_obj.sentiment.polarity)
lyrics_df['polarity'] = lyrics_df['polarity'].apply(lambda x: (x + 1) / 2) # converts (-1,1) score to (0,1)

### JOIN DATA ###
df = pd.merge(chart_df, spotify_df, left_on='spotifyID', right_on = 'track_uri', how='inner')
df = pd.merge(df, lyrics_df, left_on='spotifyID', right_on = 'spotifyID', how='inner')


### MARKET DATA DATA ###

df_month = df.groupby(['year', 'month', 'decade'])[['happy_index', 'valence', 'energy', 'polarity']].mean().reset_index()

### IMPORT SNP ###
snp_df = pd.read_csv('../data/daily_snp500.csv')
snp_df['Date'] = pd.to_datetime(snp_df[('Date')])
snp_df['year'] = snp_df['Date'].dt.year
snp_df['month'] = snp_df['Date'].dt.month
snp_df['Mid'] = (snp_df['High'] + snp_df['Low'])/2

# aggregate snp
snp_h = snp_df.groupby(['year', 'month'])['High'].max().reset_index(name = 'snp_high')
snp_l = snp_df.groupby(['year', 'month'])['Low'].min().reset_index(name = 'snp_low').drop(['year', 'month'], axis = 1)
snp_m = snp_df.groupby(['year', 'month'])['Mid'].mean().reset_index(name = 'snp_mid').drop(['year', 'month'], axis = 1)
snp_vol = snp_df.groupby(['year', 'month'])['Volume'].sum().reset_index(name = 'snp_vol').drop(['year', 'month'], axis = 1)
snp_month_df = pd.concat([snp_h, snp_l, snp_m, snp_vol], axis=1)

# merge snp with music data
df_month = pd.merge(df_month, snp_month_df)

# import consumer confidence index
cci_df = pd.read_csv('../data/cci.csv')
# only keep important information
cci_df = cci_df[cci_df['LOCATION'] == 'USA'][['TIME', 'Value']]
cci_df['TIME'] = pd.to_datetime(cci_df['TIME'])
cci_df['month'] = cci_df['TIME'].dt.month
cci_df['year'] = cci_df['TIME'].dt.year
cci_df = cci_df.rename(index=str, columns = {'Value': 'cci_value'})
cci_df = cci_df.drop('TIME', axis = 1)

# merge cci with music data
df_month = pd.merge(df_month, cci_df)