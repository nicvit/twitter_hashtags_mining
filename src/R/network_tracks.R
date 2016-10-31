library(rmongodb)

mongo = mongo.create()
db.coll <- 'snowball.net_0'
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
# transform into a term-term adjacency matrix
# ajx_mx_occ <- hash_in_tweet %*% t(hash_in_tweet)
ajx_mx_occ <- tcrossprod(hash_in_tweet)
# diagonal it's the total number an hashtag compare, considering it alone and wit others
# NORMALIZE
# tot_occ_feat <- diag(ajx_mx_occ)
diag(ajx_mx_occ) <- 0 # Diagonal should be the total occurrence of a feature; but it doesn't seems so .... removed, we are interested in relationship with the otheres
ajx_mx_prob <- t(ajx_mx_occ/apply(ajx_mx_occ, 1, sum)) # NOTE: rows are divided, columns don't have mening animore --> transpose: columns have meaning
ajx_mx_prob_percent <- ajx_mx_prob*100

plot(sort(ajx_mx_prob_percent[,"ecig"], decreasing =  T), log = 'x')


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################

track<-c('ecig', 'vaping', 'vape', 'vaporizer', 'marijuana', 'sorrynotsorry', 'eliquid', 'ecigs', 'vapeporn', 'cannabis') # INITIALIZE track called "track0"

########################################################################################################################################################
track0 <- c('ecig', 'vaping', 'vape', 'vaporizer', 'marijuana', 'sorrynotsorry', 'eliquid', 'ecigs', 'vapeporn', 'cannabis')
t <- ajx_mx_prob[, track0]
n<-c()
for (i in track0) {
  new_names <- rownames(t[t[,i]>0.02,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track1<-setdiff(n,track) # SEARCH new track
track1
remove("n")

track <- unique(c(track0, track1)) # UPDATE main track

write.csv(track1, file = "~/Desktop/twitter_data_analysis/scripts/R/track1.csv")
write.csv(track1, file = "~/Desktop/twitter_data_analysis/develop/Py/track1.csv")

########################################################################################################################################################
track1 # previous track
t <- ajx_mx_prob[, track]
n<-c()
for (i in track) {
  new_names <- rownames(t[t[,i]>0.05,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track2<-setdiff(n,track) # SEARCH new track
track2
remove("n")

track <- unique(c(track, track2)) # UPDATE main track

write.csv(track2, file = "~/Desktop/twitter_data_analysis/scripts/R/track2.csv")
write.csv(track2, file = "~/Desktop/twitter_data_analysis/develop/Py/track2.csv")

########################################################################################################################################################
t <- ajx_mx_prob[, track]
n<-c()
for (i in track) {
  new_names <- rownames(t[t[,i]>0.05,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track3<-setdiff(n,track) # SUBSTITUTE, new track (previous_track+1)
track3
remove("n")

track <- c(track, track3) # SUBSTITUTE, UPDATE main track

write.csv(track3, file = "~/Desktop/twitter_data_analysis/scripts/R/track3.csv") # SUBSTITUTE, name of new track in BOTH PLACES
write.csv(track3, file = "~/Desktop/twitter_data_analysis/develop/Py/track3.csv") # SUBSTITUTE, name of new track

########################################################################################################################################################
t <- ajx_mx_prob[, track]
n<-c()
for (i in track) {
  new_names <- rownames(t[t[,i]>0.05,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track4<-setdiff(n,track) # SUBSTITUTE, new track (previous_track+1)
track4
remove("n")

track <- c(track, track4) # SUBSTITUTE, UPDATE main track

write.csv(track4, file = "~/Desktop/twitter_data_analysis/scripts/R/track4.csv") # SUBSTITUTE, name of new track in BOTH PLACES
write.csv(track4, file = "~/Desktop/twitter_data_analysis/develop/Py/track4.csv") # SUBSTITUTE, name of new track

########################################################################################################################################################
# DONE the 4th iteration, the below code it's the next to be running (It start the 5th level search)
# t <- ajx_mx_prob[, track]
# n<-c()
# for (i in track) {
#   new_names <- rownames(t[t[,i]>0.05,])
#   for (j in new_names) {
#     n<-c(n,j)
#   }
# }
# remove(list =  c("i", "j", "new_names", "t"))
# 
# n<-unique(n)
# track5<-setdiff(n,track) # SUBSTITUTE, new track (previous_track+1)
# track5
# remove("n")
# 
# track <- c(track, track5) # SUBSTITUTE, UPDATE main track
# 
# write.csv(track5, file = "~/Desktop/twitter_data_analysis/scripts/R/track5.csv") # SUBSTITUTE, name of new track in BOTH PLACES
# write.csv(track5, file = "~/Desktop/twitter_data_analysis/develop/Py/track5.csv") # SUBSTITUTE, name of new track


########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################



library(igraph)

net_core_prob<-ajx_mx_prob[track, track]
plot_net_core <- graph.adjacency(net_core_prob, mode = "undirected", weighted = TRUE)
saveAsGEXF(plot_net_core, filepath = "~/Desktop/twitter_data_analysis/scripts/R/plot_net_core")

plot_net_full_no_weights <- graph.adjacency(ajx_mx_prob, mode = "undirected")
saveAsGEXF(plot_net_full_no_weights, filepath = "~/Desktop/twitter_data_analysis/scripts/R/plot_net_full_no_weights")

plot_net_full_si_weights <- graph.adjacency(ajx_mx_prob_percent, mode = "undirected", weighted = TRUE)
saveAsGEXF(plot_net_full_si_weights, filepath = "~/Desktop/twitter_data_analysis/scripts/R/TRY.gexf")

plot_net_full_si_weights_occ <- graph.adjacency(ajx_mx_occ, mode = "undirected", weighted = TRUE)
saveAsGEXF(plot_net_full_si_weights_occ, filepath = "~/Desktop/twitter_data_analysis/scripts/R/plot_net_full_si_weights_occ")

