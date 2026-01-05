#! /usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
strategies = c('rotation','hop','hop_rotation')

metrics = c('ALTITUDE','CHUNK_PROCESSING_TIME','KVC_BYTES','SERVERS')

for (metric in metrics) { 
  data.rotation = read.table(paste('results/rotation.',metric,'.dat',sep=""),header=T)
  data.hop = read.table(paste('results/hop.',metric,'.dat',sep=""),header=T)
  data.hoprotation = read.table(paste('results/hop_rotation.',metric,'.dat',sep=""),header=T)
  filename = paste("plots/",metric,"summary.png",sep="")
  filename = gsub("_","",filename)
  png(filename)
  ymin = min(data.rotation$MAX,data.hop$MAX,data.hoprotation$MAX)
  ymax = max(data.rotation$MAX,data.hop$MAX,data.hoprotation$MAX)
  plot(data.rotation[,1],data.rotation$MAX,ylim=c(ymin,ymax),ylab="Time(s)",main=metric,xlab=metric)
  lines(data.rotation[,1],data.rotation$MAX,col="red")
  points(data.rotation[,1],data.rotation$MAX,col="red")
  lines(data.hop[,1],data.hop$MAX,col="blue")
  points(data.hop[,1],data.hop$MAX,col="blue")
  lines(data.hoprotation[,1],data.hoprotation$MAX,col="green")
  points(data.hoprotation[,1],data.hoprotation$MAX,col="green")
  legend("bottomright",legend=c("rotation","hop","hoprotation"),col=c("red","blue","green"),lty=1)
dev.off()
}
