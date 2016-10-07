wd <- "C:/git/dc-michelin-challenge/submissions/AlexMiller/supplemental_data/"
setwd(wd)

#The list of Bib Gourmand restaurants were released today. A total of 19 for DC. Is there something we can learn from ratios?

dat <- read.csv("ny_stars.csv")
latest <- subset(dat,year==2016 & stars>0)
ny.ratio <- nrow(latest)/190

dat <- read.csv("chi_stars.csv",na.strings="Closed")
latest <- subset(dat,year==2016 & stars>0)
chi.ratio <- nrow(latest)/58

average <- mean(c(chi.ratio,ny.ratio))

dc.bib <- 19
dc.stars <- dc.bib*average
#Perhaps 7-8 starred restaurants?