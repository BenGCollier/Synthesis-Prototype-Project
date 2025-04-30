Lab3<-read.csv(file.choose(),header=T)
str(Lab3)
Column6=gsub(",","",Lab3$MedianHouseholdIncome)
Lab3$MedianHouseholdIncome<-as.numeric(Column6)
str(Lab3)
summary(Lab3)
Lab3_2<-na.omit(Lab3)
summary(Lab3_2)
Lab3_2[!duplicated(Lab3_2), ]
Lab3_3<-Lab3_2[!duplicated(Lab3_2), ]
str(Lab3_3)
Column1=gsub("[A-Z]","0",Lab3_3$RegionID)
Lab3_3$RegionID<-Column1
str(Lab3_3)
write.csv(Lab3_3, file - "Lab3_3.csv")