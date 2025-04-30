#import training dataset
Exam1<-read.csv(file.choose(), header=T, stringsAsFactors = T)
#import training dataset
Exam1_predict<-read.csv(file.choose(), header=T,stringsAsFactors = T)
#Structure of both datasets
str(Exam1)
str(Exam1_predict)
#Remove consideration of GBP from the the currency attribute
Exam1_2<-Exam1 [Exam1$Currency!='GBP',]
#Check if GBP records are removed
summary(Exam1_2)
str(Exam1_2)
#Remove currency attribute
Exam1New <-subset (Exam1_2, select=-Currency)
#Check if currency is removed
str(Exam1New)
#On the OpenPrice attribute, replace missing values
Exam1New$OpenPrice[which(is.na(Exam1New$OpenPrice))]<-min(Exam1New$OpenPrice,na.rm=T)
#Check if missing values are replaced
summary(Exam1New)

#Installing party package and loading library
install.packages("party")
library(party)
#Creation of decision tree with Competitive as target using training dataset
DT<-ctree(Competitive ~., data=Exam1New)
#Applying the DT for prediction, storing it in R_DT
R_DT<-predict(DT,Exam1_predict)
#Checking predictions
summary(R_DT)

#Loading library
library(e1071)
#Creation of NB model with Competitive as target using training dataset
NB<-naiveBayes(Competitive ~., data=Exam1New)
#Applying the NB for prediction, storing it in R_NB
R_NB<-predict(NB, Exam1_predict)
#Checking predictions
summary(R_NB)

#Creation of the LR model Competitive as target using training dataset
LR<-glm(Competitive ~., data=Exam1New, family=binomial)
#Applying the LR for prediction, storing it in R_LRP
R_LRP<-predict(LR, Exam1_predict,type="response")
#Converting probabilities to the prediction class and converting to a factor
R_LR<-as.factor(ifelse(R_LRP > 0.5, "yes", "no"))
#Checking predictions
summary(R_LR)

#Loading the library
library(nnet)
#Setting seed
set.seed(1000)
#Creation of the NN model Competitive as target using training dataset
NN<-nnet(Competitive ~., data=Exam1New, size=8, maxit=10000)
#Applying the NN for prediction, storing it in R_NNP
R_NNP<-predict(NN, Exam1_predict)
##Converting probabilities to the prediction class and converting to a factor
R_NN<-as.factor(ifelse(R_NNP > 0.5, "yes", "no"))
#Checking predictions
summary(R_NN)

R_Predict<-rbind (as.vector(R_DT),as.vector(R_NB),as.vector(R_LR),as.vector(R_NN))
R_DF<-as.data.frame(t (R_Predict))
colnames (R_DF) <-c("R_DT", "R_NB", "R_LR", "R_NN")
write.csv(R_DF,"R_DF.CSV")
