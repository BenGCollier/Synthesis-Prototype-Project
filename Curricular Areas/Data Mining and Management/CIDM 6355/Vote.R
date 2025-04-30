Lab5Train<-read.csv(file.choose(),header=T,stringsAsFactors=T) 
Lab5Predict<-read.csv(file.choose(), header=T, stringsAsFactors=T)
names(Lab5Train)
dim(Lab5Train)
summary(Lab5Train)
install.packages("e1071")
library(e1071)
Lab5NB<-naiveBayes(education.spending ~., data=Lab5Train)
Lab5NB
Lab5score <-predict (Lab5NB, Lab5Predict)
Lab5score
summary(Lab5score)
Score<-data.frame(Lab5score)
Lab5Predict$education.spending<-Score$Lab5score
Lab5Predict

Lab5Train$education.spending[Lab5Train$education.spending=="abstain"]<-"n"
LogModel<-glm(education.spending ~ .,family= "binomial", data=Lab5Train)
summary(LogModel)
Lab5ScoreLR <-predict(LogModel, Lab5Predict,type="response")
round(Lab5ScoreLR, 3)
Lab5ScoreLR>0.5
sum(Lab5ScoreLR>0.5)

