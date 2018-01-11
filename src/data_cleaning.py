import pandas as pd
import numpy as np
from textblob import TextBlob

def import_clean_chart_data(file, keep_top_10 = True):
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
    if keep_top_10:
        chart_df = chart_df[chart_df['rank'] < 11]

    return chart_df


### SPOTIFY DATA ###
def import_clean_spotify_data(file):
    spotify_df = pd.read_csv(file)
    spotify_df = spotify_df.drop_duplicates() # remove one spotify dup
    spotify_df['maj_minor'] = spotify_df['key_mode'].str.split(' ', 1).str[1]
    return spotify_df


### LYRICS DATA ###

def import_clean_lyrics_data(file):
    lyrics_df = pd.read_csv(file)
    lyrics_df = lyrics_df[lyrics_df['Source'].notnull()] # remove songs without lyrics

    # Create TextBlob object. Extract polarity score
    lyrics_df['tb_obj'] = lyrics_df['Lyrics'].apply(lambda lyric: TextBlob(lyric))  # takes a bit to run
    lyrics_df['polarity'] = lyrics_df['tb_obj'].apply(lambda tb_obj: tb_obj.sentiment.polarity)
    lyrics_df['polarity'] = lyrics_df['polarity'].apply(lambda x: (x + 1) / 2)  # converts (-1,1) score to (0,1)
    return lyrics_df

### JOIN DATA ###
def join_data(chart_df, spotify_df, lyrics_df):
    df = pd.merge(chart_df, spotify_df, left_on='spotifyID', right_on = 'track_uri', how='inner')
    df = pd.merge(df, lyrics_df, left_on='spotifyID', right_on = 'spotifyID', how='inner')
    return df

# ### MARKET DATA DATA ###

def group_data_by_month(df):
    return df.groupby(['year', 'month', 'decade'])[['happy_index', 'valence', 'energy', 'polarity']].mean().reset_index()

# ### IMPORT SNP ###

def import_clean_snp_data(file):
    snp_df = pd.read_csv(file)
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
    return snp_month_df


def import_clean_cci_data(file):
    # import consumer confidence index
    cci_df = pd.read_csv(file)
    # only keep important information
    cci_df = cci_df[cci_df['LOCATION'] == 'USA'][['TIME', 'Value']]
    cci_df['TIME'] = pd.to_datetime(cci_df['TIME'])
    cci_df['month'] = cci_df['TIME'].dt.month
    cci_df['year'] = cci_df['TIME'].dt.year
    cci_df = cci_df.rename(index=str, columns = {'Value': 'cci_value'})
    cci_df = cci_df.drop('TIME', axis = 1)
    return cci_df

def merge_all_data(df_month, snp_month_df, cci_df):
    # merge snp with music data
    df_month = pd.merge(df_month, snp_month_df)
    # merge cci with music data
    df_month = pd.merge(df_month, cci_df)
    return df_month

def main():
    chart_df = import_clean_chart_data('../data/all_charts.csv')
    spotify_df = import_clean_spotify_data('../data/spotify_data.csv')
    lyrics_df = import_clean_lyrics_data('../data/lyrics.csv')
    df = join_data(chart_df, spotify_df, lyrics_df)
    df_month = group_data_by_month(df)
    snp_month_df = import_clean_snp_data('../data/daily_snp500.csv')
    cci_df = import_clean_cci_data('../data/cci.csv')
    df_month = merge_all_data(df_month, snp_month_df, cci_df)
    # print(chart_df.shape[0], spotify_df.shape[0], lyrics_df.shape[0])
if __name__ == '__main__':
    main()