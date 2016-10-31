library(ggplot2)

starting_list = c('ecig', 'vaping', 'vape', 'vaporizer', 'marijuana', 'sorrynotsorry', 'eliquid', 'ecigs', 'vapeporn', 'cannabis') 

ajx_mx_occ <- hash_in_tweet %*% t(hash_in_tweet)
# diagonal it's the total number an hashtag compare, considering it alone and wit others
# NORMALIZE
tot_occ_feat <- diag(ajx_mx_occ)
diag(ajx_mx_occ) <- 0
ajx_mx_prob <- ajx_mx_occ/tot_occ_feat # NOTE: rows are divided, columns don't have mening animore
ajx_mx_prob[ajx_mx_prob>=1] <- 1

ajx_df <- as.data.frame(t(ajx_mx_prob)) # NOTE: here columns are significant

plot(sort(ajx_df$marijuana, decreasing =  T), log = 'x')



ecig <- ajx_mx_prob['ecig',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['vaping',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['vape',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['vaporizer',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['marijuana',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['sorrynotsorry',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['eliquid',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['ecigs',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['vapeporn',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]

ecig <- ajx_mx_prob['cannabis',]
ecig <- sort(ecig[ecig<1 & ecig >0], decreasing = T)
quantile(ecig, probs = c(.90,.91,.92,.93,.94,.95,.96,.97,.98,.99))
ecig[1:60]


################################

# ecig <- row.names(subset(ajx_df, ecig >= unname(quantile(ajx_df$ecig, c(.95))) & ecig <= unname(quantile(ajx_df$ecig, c(1))), select = ecig))
ecig <- row.names(subset(ajx_df, ecig >= unname(quantile(ajx_df$ecig, c(.95))), select = ecig))
vaping <- row.names(subset(ajx_df,vaping>=unname(quantile(ajx_df$vaping, c(.95))), select = vaping))
vape <- row.names(subset(ajx_df,vape>=unname(quantile(ajx_df$vape, c(.95))), select = vape))
vaporizer <- row.names(subset(ajx_df,vaporizer>=unname(quantile(ajx_df$vaporizer, c(.95))), select = vaporizer))
marijuana <- row.names(subset(ajx_df,marijuana>=unname(quantile(ajx_df$marijuana, c(.95))), select = marijuana))
sorrynotsorry <- row.names(subset(ajx_df,sorrynotsorry>=unname(quantile(ajx_df$sorrynotsorry, c(.95))), select = sorrynotsorry))
eliquid <- row.names(subset(ajx_df,eliquid>=unname(quantile(ajx_df$eliquid, c(.95))), select = eliquid))
ecigs <- row.names(subset(ajx_df,ecigs>=unname(quantile(ajx_df$ecigs, c(.95))), select = ecigs))
vapeporn <- row.names(subset(ajx_df,vapeporn>=unname(quantile(ajx_df$vapeporn, c(.95))), select = vapeporn))
cannabis <- row.names(subset(ajx_df,cannabis>=unname(quantile(ajx_df$cannabis, c(.95))), select = cannabis))



un1 <- unique(union(ecig, vaping))
un2 <- unique(union(un1, vape))
un3 <- unique(union(un2, vaporizer))
un4 <- unique(union(un3, marijuana))
un5 <- unique(union(un4, sorrynotsorry))
un6 <- unique(union(un5, eliquid))
un7 <- unique(union(un6, ecigs))
un8 <- unique(union(un7, vapeporn))
un9 <- unique(union(un8, cannabis))

track1 <- setdiff(un9,starting_list)

write.csv(track1, file = "track1.csv")

