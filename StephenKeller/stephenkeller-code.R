#***********************BUILD LIST OF RESTAURANTS********************
#list of dc restaurants ext:xls   google search
#downloaded data and saved it as a csv 
df<-read.csv('restDC.csv',header=TRUE)

#Need to remove the list of smaller restaurants already chosen
#https://www.washingtonpost.com/news/going-out-guide/wp/2016/10/06/michelin-announces-its-first-d-c-honors-the-bib-gourmand-list-of-affordable-restaurants/
#I made these into a data table
notApp<-read.csv('notApplicable.csv',header=TRUE)

#Use michelin guide numbers from other cities to guess the approx 
#size of the list 
#https://en.wikipedia.org/wiki/Michelin_Guide
#Create data table with copy from clipboard 
michList<-read.csv('numberOfRest.csv',header=TRUE)

#using basic exploratory analysis, we believe that the number of 
#restaurants are: #1 star = 20, 2 star = 7 , 3 star = 1 or 2 
#See Public Tableau Review of the Data
#https://public.tableau.com/profile/publish/BibGourmand/BibGourmandtoNumberofRestaurants#!/publish-confirm
#We note the number of new bib gourmand selections and save those
#http://www.prnewswire.com/news-releases/michelin-reveals-washington-dcs-bib-gourmand-selections-ahead-of-inaugural-michelin-guide-debut-next-week-300340721.html#continue-jump

#Recent top 100 list
others<-read.csv('hundredExtra.csv',header=TRUE)

#*******************************NARROW AND BUILD FINAL POTENTIAL LIST********
library(dplyr)
#take left four letters for each rest. 
df$quickName <-tolower(as.character(substr(df$Restaurant,1,8)))
others$quickName <-tolower(as.character(substr(others$Restaurant,1,8)))
#semi_join gives us restaurants in two lists 
new<-semi_join(df,others,"quickName")
new<-new%>%left_join(others,"quickName")

#shave off not applicable restaurants
notApp$quickName<-tolower(as.character(substr(notApp$notApplicable,1,8)))
notApp$indicator<-1
new<-new%>%left_join(notApp,"quickName")
#filter out non-DC locations and items on another list
new<-new%>%filter(is.na(indicator))
new<-new%>%filter(State=="DC")
#testing for uniqueness
test_unique<-unique(new)
tester<-new%>%group_by(quickName)%>%summarize(n=n())

#***********************************create final file 
final_df<-new%>%select(restaurant=Restaurant.x)%>%mutate(stars=1)
write.csv(final_df,"submission.csv",row.names = FALSE)
