# retrive documents from DB
library(mongolite)
mongo <- mongo(collection = "net_00", db = "sn_sp", url = "mongodb://localhost",
               verbose = TRUE)
h_df <- mongo$find('{}', fields = '{"_id":true,"hashtags":true}')


# build df | tweet_id | hashtag | (long format: tweet_id is repeated for every hashtag contained)
df_th <- data.frame()

for(d in 1:length(coll$`_id`)){ 
  
  hashtag <- as.vector(unlist(coll$hashtags[[d]]))
  tweet_id <- rep(coll$`_id`[d], times = length(hashtag)) 
  df <- data.frame(tweet_id, hashtag)
  
  df_th <- rbind(df_th, df)
  
}
remove(list =  c("d","hashtag", "mongo", "tweet_id"))

# buid occurrence matrix with unique tweet in rows and unique ashtag as column
hash_in_tweet <- as.matrix(xtabs(~hashtag + tweet_id, data=df_th))

# transform into a term-term adjacency matrix
ajx_mx_occ <- tcrossprod(hash_in_tweet)

# normalize
diag(ajx_mx_occ) <- 0 
ajx_mx_prob <- t(ajx_mx_occ/apply(ajx_mx_occ, 1, sum)) 
ajx_mx_prob_percent <- ajx_mx_prob*100

scatter(sort(ajx_mx_prob[,"vape"], decreasing =  T), log = 'x', main  = "#vape", xlab = "log(hashtag_id)", ylab = "P(hashtag_id|#vape)", type = "o")
plot(sort(ajx_mx_prob[,"tobacco"], decreasing =  T), log = 'x', main  = "#tobacco" , sub = "Hashtags _id on x axis in decreasing order for values P(hashtag_id|#vape)" , xlab = "log(hashtag_id)", ylab = "P(hashtag_id|#vape)")

library(ggplot2)
library(gridExtra)
library(ggthemes)

ajx_df_prob <- as.data.frame(ajx_mx_prob)
p1 <- ggplot(ajx_df_prob, aes(x = , y = vape))
p1 + geom_point()
# change branch out by sampling those that over 1% probability of appearing with starting ones

########################################################################################################################################################
########################################################################################################################################################
track0 <- c('ecig', 'vaping', 'vape', 'vaporizer', 'marijuana', 'sorrynotsorry', 'eliquid', 'ecigs', 'vapeporn', 'cannabis')
t <- ajx_mx_prob_percent[, track0]
n<-c()
for (i in track0) {
  new_names <- rownames(t[t[,i]>1,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track1<-setdiff(n,track0) # SEARCH new track
track1
remove("n")

track <- unique(c(track0, track1)) # UPDATE main track

write.csv(track1, file = "~/Desktop/twitter_data_analysis/scripts/R/track1.csv")
write.csv(track1, file = "~/Desktop/twitter_data_analysis/develop/Py/track1.csv")

########################################################################################################################################################
########################################################################################################################################################
t <- ajx_mx_prob_percent[, track]
n<-c()
for (i in track) {
  new_names <- rownames(t[t[,i]>1,])
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
########################################################################################################################################################
t <- ajx_mx_prob_percent[, track]
n<-c()
for (i in track) {
  new_names <- rownames(t[t[,i]>1,])
  for (j in new_names) {
    n<-c(n,j)
  }
}
remove(list =  c("i", "j", "new_names", "t"))

n<-unique(n)
track3<-setdiff(n,track) # SEARCH new track
track3
remove("n")

track <- unique(c(track, track3)) # UPDATE main track
# 
# write.csv(track3, file = "~/Desktop/twitter_data_analysis/scripts/R/track3.csv")
# write.csv(track3, file = "~/Desktop/twitter_data_analysis/develop/Py/track3.csv")
# 
# ########################################################################################################################################################
# ########################################################################################################################################################

track<-setdiff(track, track3)

track01<-c(track0, track1)

track_all<-unique(c(track, track3))

final_net<-ajx_mx_prob_percent[track, track]

library(igraph)

plot_final_net <- graph.adjacency(final_net, mode = "undirected", weighted = TRUE)
saveAsGEXF(plot_final_net, filepath = "~/Desktop/GFX/plot_final_track_012.gexf")



t0<-rep("t0", 10)
t1<-rep("t1", 73)
t2<-rep("t2", 452)
t3<-rep("t3", 1538)

t0_n<-as.data.frame(cbind(track0, t0))
colnames(t0_n)<-c("node_name", "track_name")
t1_n<-as.data.frame(cbind(track1, t1))
colnames(t1_n)<-c("node_name", "track_name")
t2_n<-as.data.frame(cbind(track2, t2))
colnames(t2_n)<-c("node_name", "track_name")
t3_n<-as.data.frame(cbind(track3, t3))
colnames(t3_n)<-c("node_name", "track_name")


name_track<-data.frame()
name_track<-rbind(name_track, t0_n)
name_track<-rbind(name_track, t1_n)
name_track<-rbind(name_track, t2_n)
name_track<-rbind(name_track, t3_n)

write.csv(name_track, file = "~/Desktop/GFX/name_track.csv")
