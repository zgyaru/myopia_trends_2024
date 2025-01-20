
library(ggplot2)

#### Figure A
data = readRDS('E:/zyr/myopia/data_2019_2024.rds')
rates = c()
groups = c()
times = c()
for(d in names(data)){
  print(d)
  rates = c(rates, mean(data[[d]]$myopia))
  rates = c(rates, mean(data[[d]]$high_myopia,na.rm = T))
  print(rates)
  groups = c(groups, 'Myopia')
  groups = c(groups, 'High Myopia')
  times = c(times, d)
  times = c(times, d)
}
plot_data = data.frame('rates' = rates*100,
                       'groups' = groups,
                       'times' = times
                       )
plot_data


### Figure B
SER = c()
times = c()
for(d in names(data)){
  print(d)
  SER = c(SER, mean(data[[d]]$worse_SE,na.rm = T))
  times = c(times, d)
}
plot_data = data.frame('SER' = SER,
                       'times' = times
)
plot_data


### Figure C
folds = c()
times = c()
grades = c()
for(g in 1:12){
  baseline = mean(data[['2019']]$myopia[data[['2019']]$grade == g])
  folds = c(folds,mean(data[['2020']]$myopia[data[['2020']]$grade == g])/baseline)
  folds = c(folds,mean(data[['2021']]$myopia[data[['2021']]$grade == g])/baseline)
  folds = c(folds,mean(data[['2022']]$myopia[data[['2022']]$grade == g])/baseline)
  folds = c(folds,mean(data[['2023']]$myopia[data[['2023']]$grade == g])/baseline)
  folds = c(folds,mean(data[['2024']]$myopia[data[['2024']]$grade == g])/baseline)
  times = c('2020','2021','2022','2023','2024')
  grades = c(grades,rep(g,5))
}
baseline = mean(data[['2019']]$myopia)
folds = c(folds,mean(data[['2020']]$myopia)/baseline)
folds = c(folds,mean(data[['2021']]$myopia)/baseline)
folds = c(folds,mean(data[['2022']]$myopia)/baseline)
folds = c(folds,mean(data[['2023']]$myopia)/baseline)
folds = c(folds,mean(data[['2024']]$myopia)/baseline)
times = c('2020','2021','2022','2023','2024')
grades = c(grades,rep('all',5))
plot_data = data.frame(folds = folds,
                       times = times,
                       grades = grades)
plot_data[which(plot_data$grades == 1),]
plot_data[which(plot_data$grades == 'all'),]
plot_data



### Figure D
values = c()
groups = c()
times = c()
for(d in names(data)){
  print(d)
  values = c(values, mean(data[[d]]$myopia[data[[d]]$grade == 1]))
  values = c(values, mean(data[[d]]$worse_SE[data[[d]]$grade == 1],na.rm = T))

  groups = c(groups, 'Myopia')
  groups = c(groups, 'SER')
  times = c(times, d)
  times = c(times, d)
}
plot_data = data.frame('values' = values,
                       'groups' = groups,
                       'times' = times
)
plot_data
