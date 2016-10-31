# set working directory
setwd("~/Desktop/twitter_data_analysis/scripts/R")
# query mongo and obtain a list
library(rmongodb)

mongo = mongo.create()
db.coll <- 'network.tracks'
cursor <- mongo.find(mongo, db.coll, query = '{}', fields = '{"_id":true,"entities.hashtags.text":true}')
coll <- mongo.cursor.to.list(cursor)

# clean


# build df |tweet_id|hashtag (long format: tweet_id is repeated for every hashtag contained)
tweet_id <- c()
hashtag<-c()
final_df <- data.frame(tweet_id, hashtag)

for(d in seq_along(coll)){
  
  doc<-coll[[d]]
  
  tweet_id <- c()
  hashtag<-c()
  for(i in seq_along(doc$entities$hashtags)){
    tweet_id <- append(tweet_id, c(doc$`_id`))
    hashtag <- append(hashtag, c(tolower(doc$entities$hashtags[i][[1]]$text)))
  }
  temp_df <- data.frame(tweet_id, hashtag)
  
  final_df <- rbind(final_df, temp_df)
  
  
  
}

remove(list =  c("coll", "cursor", "d", "db.coll", "doc", "hashtag", "i", "mongo", "temp_df", "tweet_id"))

# buid occurrence matrix with unique tweet in rows and unique ashtag as column
hash_in_tweet <- as.matrix(xtabs(~hashtag + tweet_id, data=final_df))
#Transform Data into an Adjacency Matrix
# change it to a Boolean matrix
# hash_in_tweet[hash_in_tweet>=1] <- 1
# transform into a term-term adjacency matrix
ajx_mx_occ <- hash_in_tweet %*% t(hash_in_tweet)
# diagonal it's the total number an hashtag compare, considering it alone and wit others
# NORMALIZE
tot_occ_feat <- diag(ajx_mx_occ)
diag(ajx_mx_occ) <- 0
ajx_mx_prob <- ajx_mx_occ/tot_occ_feat
ajx_mx_prob[ajx_mx_prob>=1] <- 1
# inspect terms numbered 5 to 10
ajx_mx_prob[5:10,5:10]
# plot network
library(igraph)
#as_adj_mx <- as_adjacency_matrix(results, sparse = TRUE)
g <- graph.adjacency(ajx_mx_prob, mode = "undirected", weighted = TRUE)


saveAsGEXF(g, filepath = "track1_norm.gexf")

