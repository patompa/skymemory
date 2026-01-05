#! /usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
data = read.table(args[1],header=T)
title = colnames(data)[1]
strategy = args[2]
filename = paste("plots/",strategy,title,".png",sep="")
filename = gsub("_","",filename)
png(filename)
plot(data[,1],data$MAX,ylab="Time(s)",main=paste(strategy,title),xlab=title)
lines(data[,1],data$MAX)
dev.off()
