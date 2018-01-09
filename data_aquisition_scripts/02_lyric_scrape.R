library(tidyverse)
library(RCurl)
library(XML)
library(stringr)

df <- read_csv('data/all_charts.csv')

df %>% glimpse()

allthesongs <- df %>% 
  select(Song = title,
         Artist = artist, 
         spotifyID) %>% 
  distinct()

allthesongs$Song <- gsub('\\"', "", allthesongs$Song)
allthesongs$Song <- tolower(gsub("[^[:alnum:] ]", "", allthesongs$Song))
allthesongs$Song <- gsub("\\'", "", iconv(allthesongs$Song, to='ASCII//TRANSLIT')) # fix special accent chars

allthesongs$Artist <- tolower(gsub("[^[:alnum:] ]", "", allthesongs$Artist))
allthesongs$Artist <- gsub("'e", "e", iconv(allthesongs$Artist, to='ASCII//TRANSLIT')) # fix special accent chars
allthesongs$Artist<- gsub("'o", "o", allthesongs$Artist)

# new variables
allthesongs$Lyrics <- ""
allthesongs$Source <- ""

if(file.exists('data/lyrics.csv')) {
  lyrics_df <- read_csv('data/lyrics.csv')
  lyrics_df %>% glimpse()
  allthesongs <- allthesongs %>% 
    anti_join(lyrics_df, by = c('Song', 'Artist', 'spotifyID'))
}

################### SCRAPE THE LYRICS ###################
### source: multiple. 1=metorlyics.com, 3=songlyrics.com, 5=lyricsmode.com
for (s in 1:length(allthesongs$Song))  {
     
     lyrics <- "Not set yet."
     results <- 12 # arbitrary number
     
     # clean up the artist field to fit in the URL
     artist <- strsplit(allthesongs$Artist[s], " featuring | feat | feat. | with | duet | and ")
     artist <- unlist(artist)[[1]]
     artist2 <- gsub("the ", "", artist)
     firstletter <- substring(artist2, 1, 1)
     
     # make URLs
     metroURL <- paste("http://metrolyrics.com/",allthesongs$Song[s],"-lyrics-",artist2,".html",sep="")
     songURL <- paste("http://songlyrics.com/",artist2,"/",allthesongs$Song[s],"-lyrics",sep="")
     modeURL <- paste("http://www.lyricsmode.com/lyrics/", firstletter, "/", artist2, "/", allthesongs$Song[s], 
                      ".html", sep="")
     
     
     URLs <- c(metroURL, songURL, modeURL)
     
     lyriclocs <- c("//div[@id='lyrics-body-text']", 
                    "//p[@id='songLyricsDiv']", 
                    "//p[@id='lyrics_text']")
     
     for (b in 1:length(URLs)) {
          allthesongs$Lyrics[s] <- "Not set yet."
          
          results <- 12 # arbitrary number
          
          if(b!=3) URL <- tolower(gsub(" ", "-", URLs[b]))
          if(b==3) URL <- URLs[b]
          
          tryCatch({ 
               results <- htmlTreeParse(URL, useInternal=TRUE, isURL=TRUE)
               lyrics <- xpathSApply(results, lyriclocs[b], xmlValue) },
               error = function(x) { 
                    message(paste(s, "failed")) 
                    
                    allthesongs[s,] %>% 
                    mutate(Lyrics = gsub("\\\n|\\\t"," ", Lyrics),
                           Lyrics = tolower(gsub("[^[:alnum:] ]", "", Lyrics))) %>% 
                    write_csv('data/lyrics.csv', append = TRUE)
                 },
               finally={ 
                    if (!is.numeric(results)) { 
                         if (length(lyrics)!=0) { 
                              allthesongs$Lyrics[s] <- lyrics[[1]]
                              message(paste(s, "success"))
                              allthesongs$Source[s] <- b
 
                              allthesongs[s,] %>% 
                                mutate(Lyrics = gsub("\\\n|\\\t"," ", Lyrics),
                                       Lyrics = tolower(gsub("[^[:alnum:] ]", "", Lyrics))) %>% 
                                write_csv('data/lyrics.csv', append = TRUE)
                              break
                         }
                    } 
               }) # end tryCatch
     } # end URL for
} # end for

# allthesongs$Lyrics <- gsub("\\\n|\\\t"," ",allthesongs$Lyrics)
# allthesongs$Lyrics <- tolower(gsub("[^[:alnum:] ]", "", allthesongs$Lyrics))
missing <- round(length(allthesongs[allthesongs$Lyrics=="not set yet", 1])/length(allthesongs[,1]), 4)*100
## 3.67% of lyrics are missing
allthesongs$Lyrics <- gsub("not set yet", "NA", allthesongs$Lyrics)
allthesongs$Lyrics <- gsub("we are not in a position to display these lyrics 
                           due to licensing restrictions sorry for the inconvenience", 
                           "NA", allthesongs$Lyrics)


################### FIX THE DUPLICATES ###################
# my scraper was duplicating values. The following lines allow me to: 
# 1 identify where the scraper stopped
# 2 remove duplicates from the script
# 3 create new lyrics csv to continue running the script


lyrics_df <- read_csv('data/lyrics_first_pass.csv')

# ID last completed song
lyrics_df %>% 
  mutate(idx = 1:n()) %>% 
  filter(Lyrics != 'not set yet') %>% 
  tail(1) %>% 
  pull(idx) -> last_var
  # first pass 6szyOE3tMWE8jIukMNK8lY ~ 14333

# df of where the last successful lyrics were pulled (likely where script crashed)
not_pulled_df <- lyrics_df %>% 
  slice(last_var+1:n()) %>%
  distinct()

# has_lyrics // filter out anything with no source or bogus lyric holders
has_lyrics_df <- lyrics_df %>% 
  filter(!is.na(Source), 
         !str_detect(Lyrics, 'we do not have the lyrics for'))

# all instances without lyrics (including true negatives) distinctified.
no_lyrics_w_pos_dups <- lyrics_df %>% 
  filter(is.na(Source)) %>% 
  distinct()

# filtering join to remove no_lyrics where there was a positive
no_lyrics <- no_lyrics_w_pos_dups %>% 
  anti_join(has_lyrics_df, by = c('Song', 'Artist'))
  
# Stack pulled and no lyrics availible. Remove subset of to-be pulled data
binded <- has_lyrics_df %>% 
  bind_rows(no_lyrics) %>% 
  anti_join(not_pulled_df, by = c('Song', 'Artist'))

# reorder to match original & write CSV

allthesongs %>% 
  inner_join(binded, by = c('Song', 'Artist')) %>% 
  select(Song, Artist, spotifyID = spotifyID.x, Lyrics = Lyrics.y, Source = Source.y) -> new_lyrics

# new_lyrics %>% count()
new_lyrics %>%  write_csv('data/lyrics.csv')
new_lyrics %>%  write_csv('data/working_lyrics2.csv')

