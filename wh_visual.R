library(hexbin)
library(RColorBrewer)
library(MASS)
w=read.csv('output.csv', header=FALSE)

df <- data.frame(w)

h <- hexbin(df)
rf <- colorRampPalette(rev(brewer.pal(11,'Spectral')))

plot(h, colramp=rf)


h1 <- hist(df$V1, breaks=25, plot=F)
h2 <- hist(df$V2, breaks=25, plot=F)
top <- max(h1$counts, h2$counts)
k <- kde2d(df$V1, df$V2, n=25)
r <- rf(32)

# margins
oldpar <- par()
par(mar=c(3,3,1,1))
layout(matrix(c(2,0,1,3),2,2,byrow=T),c(3,1), c(1,3))
image(k, col=r) #plot the image
par(mar=c(0,2,1,0))
barplot(h1$counts, axes=F, ylim=c(0, top), space=0, col='red')
par(mar=c(2,0,0.5,1))
barplot(h2$counts, axes=F, xlim=c(0, top), space=0, col='red', horiz=T)

mean(df$V1)
mean(df$V2)
