Lab10Data<-read.csv(file.choose(),header=T)
str(Lab10Data)
dim(Lab10Data)
Groups <-Lab10Data[2:303]
dim(Groups)
install.packages("arules")
library(arules)
Groups [Groups==" false"]<-NA
rules<-apriori (Groups, parameter=list (supp=0.01, minlen=2, maxlen=3, conf=0.5)) 
install.packages("arulesViz")
library(arulesViz)
plot(rules)
plot(rules, measure=c("support", "lift"), shading= "confidence")
rules2<-apriori(Groups, parameter=list(supp=0.037, minlen=2, maxlen=3, conf=0.5))
summary(rules2)
arules::inspect(sort (rules2, by = "confidence"))
as(rules2,  "data.frame")
write(rules2, file = "rules2.csv", sep = ",", quote = TRUE, row.names = FALSE)
