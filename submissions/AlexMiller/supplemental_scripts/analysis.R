wd <- "C:/git/dc-michelin-challenge/submissions/AlexMiller/supplemental_data/"
setwd(wd)

#The list of Bib Gourmand restaurants were released today. A total of 19 for DC. Is there something we can learn from ratios?

dat <- read.csv("ny_stars.csv")
latest <- subset(dat,year==2016 & stars>0)
ny.ratio <- nrow(latest)/190
ny.pop <- 8.406
ny.starred.percap <- nrow(latest)/ny.pop

dat <- read.csv("chi_stars.csv",na.strings="Closed")
latest <- subset(dat,year==2016 & stars>0)
chi.ratio <- nrow(latest)/58
chi.pop <- 2.719
chi.starred.percap <- nrow(latest)/ny.pop

average.bib <- mean(c(chi.ratio,ny.ratio))
average.pop <- mean(c(chi.starred.percap,ny.starred.percap))

dc.bib <- 19
dc.pop <- 0.658893
dc.stars.bib <- dc.bib*average.bib
dc.stars.pop <- dc.pop*average.pop
dc.stars.pop.like.ny <- dc.pop*ny.starred.percap
#Perhaps 7-8 starred restaurants?