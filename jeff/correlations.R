library(polycor)
l<-read.csv(l)
for (n in names(l)){
    l[,n]<-as.factor(l[,n])
}
a<-hetcor(l)
write.csv('tetrachoric.csv', a['correlations'])
