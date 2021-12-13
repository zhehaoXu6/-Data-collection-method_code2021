#extract information from time ,create day and month
setwd('./Data')
mt_data <- read.csv("600519.csv")
is.character(mt_data$时间)
for (i in 1:728) {
  mt_data[i,8]<-as.numeric(substring(mt_data[i,1],6,7))
  
  if(substring(mt_data[i,1],12,13)=="一")
    mt_data[i,7]<-1
  if(substring(mt_data[i,1],12,13)=="二")
    mt_data[i,7]<-2
  if(substring(mt_data[i,1],12,13)=="三")
    mt_data[i,7]<-3
  if(substring(mt_data[i,1],12,13)=="四")
    mt_data[i,7]<-4
  if(substring(mt_data[i,1],12,13)=="五")
    mt_data[i,7]<-5
  
}
names(mt_data)[c(7,8)] <- c('day','month')
# calculate N,N_1,N_2,W_1,W_2 
N<-nrow(mt_data)
N_1<-as.matrix(table(mt_data$day))
N_2<-as.matrix(table(mt_data$month))
plot(x=c(1:12),y=N_2,main="不同月份的样本量分布",type = "l",xlab="月份",ylab = "样本量",ylim=c(50,70))
W_1<-as.matrix(table(mt_data$day))/728
W_2<-as.matrix(table(mt_data$month))/728
#calculate mean var
Y_bar<-mean(mt_data$金额)
S_square<-var(mt_data$金额)

Y_bar_1<-c(NA)
S_square_1<-c(NA)
for (h in 1:5) {
  Y_bar_1[h]<-mean(mt_data[mt_data$day==h,][,4])
  S_square_1[h]<-var(mt_data[mt_data$day==h,][,4])
}
Y_bar_2<-c(NA)
S_square_2<-c(NA)
for (h in 1:12) {
  Y_bar_2[h]<-mean(mt_data[mt_data$month==h,][,4])
  S_square_2[h]<-var(mt_data[mt_data$month==h,][,4])
}
#sampling 
library(sampling)
r=0.1
alpha=0.05
#average w_1=1/5 w_2=1/12
n_1_ave<-ceiling(sum(W_1^2*S_square_1*5)/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_1*S_square_1)/N))
n_2_ave<-ceiling(sum(W_2^2*S_square_2*12)/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_2*S_square_2)/N))

day_ave_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("day"),size=rep(22,5),method="srswor"))
mean(day_ave_mt_data$金额) 
var(day_ave_mt_data$金额)

month_ave_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("month"),size=rep(9,12),method="srswor"))
mean(month_ave_mt_data$金额) 
var(month_ave_mt_data$金额)

#by ratio,w_1=W_1 w_2=W_2
n_1_rat<-ceiling(sum(W_1*S_square_1)/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_1*S_square_1)/N))
n_2_rat<-ceiling(sum(W_2*S_square_2)/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_2*S_square_2)/N))

day_rat_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("day"),size=n_1_rat*W_1,method="srswor"))
mean(day_rat_mt_data$金额) 
var(day_rat_mt_data$金额)

month_rat_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("month"),size=n_2_rat*W_2,method="srswor"))
mean(month_rat_mt_data$金额) 
var(month_rat_mt_data$金额)

#neyman
w_1<-c(NA)
w_2<-c(NA)
for (h in 1:5) {
  w_1[h]<-N_1[h]*sqrt(S_square_1[h])
}
w_1<-w_1/sum(w_1)
for (h in 1:12) {
  w_2[h]<-N_2[h]*sqrt(S_square_2[h])
}
w_2<-w_2/sum(w_2)

n_1_ney<-ceiling(sum(W_1*sqrt(S_square_1))^2/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_1*S_square_1)/N))
n_2_ney<-ceiling(sum(W_2*sqrt(S_square_2))^2/((r*Y_bar/qnorm(1-alpha/2))^2+sum(W_2*S_square_2)/N))

day_ney_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("day"),size=n_1_ney*w_1,method="srswor"))
mean(day_ney_mt_data$金额) 
var(day_ney_mt_data$金额)

month_ney_mt_data<-getdata(mt_data,strata(mt_data,stratanames=("month"),size=n_2_ney*w_2,method="srswor"))
mean(month_ney_mt_data$金额) 
var(month_ney_mt_data$金额)