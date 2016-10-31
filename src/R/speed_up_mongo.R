library(mongolite)

mongo <- mongo(collection = "net", db = "snowball", url = "mongodb://localhost",
              verbose = TRUE)

coll <- mongo$find('{}', fields = '{"_id":true,"entities.hashtags.text":true}')


# Mongo is speeded up this way BUT now it takes a lot to create the DF in long format


# build df |tweet_id|hashtag (long format: tweet_id is repeated for every hashtag contained)
tweet_id <- c()
hashtag<-c()
final_df <- data.frame(tweet_id, hashtag)

for(d in seq_len(nrow(coll$entities))){   # iterate through each tweet
  
  doc <- coll$entities$hashtags[[d]]
  id <- as.character(coll$`_id`[d])
  
  tweet_id <- c()
  hashtag <- c()
  for(i in  seq_along(doc$text)){    # iterate through each hashtag of the tweet
    
    tweet_id <- append(tweet_id, id)
    hashtag <- append(hashtag, tolower(doc$text[i]))
    
    }
  
  temp_df <- data.frame(tweet_id, hashtag)
  final_df <- rbind(final_df, temp_df)
  
}
remove(list = c("doc", "id", "tweet_id", "hashtag", "temp_df"))

remove(list =  c("mongo", "coll", "d", "i"))

# final_mx <- rbind(final_mx, c(coll$`_id`[d], tolower(coll$entities$hashtags[[d]]$text[i])))


# build df |tweet_id|hashtag (long format: tweet_id is repeated for every hashtag contained)
tweet_id <- c()
hashtag <- c()
df_th <- data.frame(tweet_id, hashtag)

for(d in 1:length(coll$`_id`)){ 
  
  tweet_id <- coll$`_id`[d]
  hashtag <- tolower(coll$entities$hashtags[[d]])
  
  df_th <- rbind(df_th, data.frame(tweet_id, hashtag))
  
}

