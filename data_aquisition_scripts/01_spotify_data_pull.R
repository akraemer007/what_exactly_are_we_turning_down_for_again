library(tidyverse)
library(magrittr)
library(spotifyr)

# import keys
source('data_aquisition_scripts/spotify_keys.R')
Sys.setenv(SPOTIFY_CLIENT_ID = spotify_id)
Sys.setenv(SPOTIFY_CLIENT_SECRET = spotify_secret)

access_token <- spotifyr::get_spotify_access_token()

# pull in main_dataframe
df <- read_csv('data/all_charts.csv') %>% 
  rename(track_uri = spotifyID)

spotify_pull <- spotifyr::get_track_audio_features(df) %>% 
  write_csv('data/spotify_data.csv')





# df %>% 
#   left_join(spotify_pull) %>% 
#   select(track_uri, danceability) %>% 
#   filter(is.na(danceability)) %>% count()
# 
# df %>%
#   count(track_uri) %>% 
#   arrange(desc(n)) %>% 
#   summarise(sum(n))
# 
# df %>% 
#   select(track_uri) %>% 
#   distinct()
# 
# df %>% 
#   # mutate(year) %>% 
#   left_join(spotify_pull) %>% 
#   select(title, artist, track_uri, rank, valence) %>% 
#   group_by(title, artist, track_uri, valence) %>% 
#   summarise(min(rank)) %>% 
#   arrange(desc(valence)) %>% 
#   head()