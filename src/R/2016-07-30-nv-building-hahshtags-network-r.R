# set working directory
setwd("~/Desktop/twitter_data_analysis/scripts/R")
# query mongo and obtain a list
library(rmongodb)

mongo = mongo.create()
db.coll <- 'final_stream.keywords_stream'
cursor <- mongo.find(mongo, db.coll, query = '{"keyword": "shisha"}', fields = '{"_id":true,"entities.hashtags.text":true}')
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
hash_in_tweet <- as.matrix(xtabs(~tweet_id + hashtag, data=final_df))

results<-matrix(0,nrow=dim(hash_in_tweet)[2],ncol=dim(hash_in_tweet)[2])    # DOUBLECHECK !!!!!
colnames(results) = levels(final_df$hashtag)
rownames(results) = levels(final_df$hashtag)

options(warnings=-1)

for(a in 1:dim(hash_in_tweet)[1]){
  tw.temp<-hash_in_tweet[a,]
  for(b in 1:(length(tw.temp)-1)){
    for(c in (b+1):(length(tw.temp))){
      if(tw.temp[b]+tw.temp[c]>1){
        
        results[b,c]<-results[b,c]+1
        results[c,b]<-results[c,b]+1
        
      }
      
    }
  }
  
}




############################################################################################
# plot network
############################################################################################


# plot network
library(igraph)

nodeNames <- levels(final_df$hashtag)
dimnames(results) <- list(nodeNames, nodeNames)

#as_adj_mx <- as_adjacency_matrix(results, sparse = TRUE)

g <- graph_from_adjacency_matrix(results, mode = "undirected")

plot(g)
# # Set edge color to light gray, the node & border color to orange
# 
# # Replace the vertex label with the node names stored in "media"
# 
# plot(g)
# 
# plot(g, edge.arrow.size=.2, edge.color="orange",
#      
#      vertex.color="orange", vertex.frame.color="#ffffff",
#      
#      vertex.label=V(g)$media, vertex.label.color="black")
# 
# 
# Compute node degrees (#links) and use that to set node size:

deg <- degree(g, mode="all")

V(g)$size <- deg*3

# We could also use the audience size value:

V(g)$size <- V(g)$audience.size*0.6

# The labels are currently node IDs.

# Setting them to NA will render no labels:

#V(g)$label <- NA

# Set edge width based on weight:

E(g)$width <- E(g)$weight/6

#change arrow size and edge color:

E(g)$arrow.size <- .2

E(g)$edge.color <- "gray80"

E(g)$width <- 1+E(g)$weight/12

l <- layout_with_lgl(g)

plot(g, layout=l)


# 
# 
# 
# #################
# layouts <- grep("^layout_", ls("package:igraph"), value=TRUE)[-1]
# 
# # Remove layouts that do not apply to our graph.
# 
# layouts <- layouts[!grepl("bipartite|merge|norm|sugiyama|tree", layouts)]
# 
# par(mfrow=c(3,3), mar=c(1,1,1,1))
# 
# for (layout in layouts) {
#   
#   print(layout)
#   
#   l <- do.call(layout, list(g))
#   
#   plot(g, edge.arrow.mode=0, layout=l, main=layout) }




# ##################
# netm <- as.matrix(as_adjacency_matrix(g)) 
# colnames(netm) <- colnames(results)
# rownames(netm) <- rownames(results)
# 
# palf <- colorRampPalette(c("gold", "dark orange")) 
# heatmap(netm, Rowv = NA, Colv = NA, col = palf(100), 
#         scale="none", margins=c(10,10) )

