install.packages("sampling")
install.packages("survey")
library(grid)
library("sampling")
library(survey)
data <- read.csv("600519.csv")
#编制抽样总体数据框
#由于共有728条数据，分为91个群*每个群8条数据
#从91个群中抽取5个群
set.seed(123)
a =rep(1:91,each = 8 )
b = 1:728
data1 = data.frame("群号"= a,"时间" = b)
data = cbind(data,data1)
#进行整群抽样
sampling:::cluster(data,clustername="群号",size=5,method="srswor",description=TRUE)

c = sampling:::cluster(data,clustername="群号",size=5,method="srswor",description=TRUE)
#从整体数据框中提取样本数据
c = getdata(data, c)
#pw为入样概率的倒数（样本权重）
pw = rep(nrow(data)/nrow(c),nrow(c))
N = 91
#设定fpc变量，为总体中的PSU的个数
fpc = rep(N, nrow(c))
fpc

agclus = as.data.frame(cbind(c,pw,fpc))

dclus <- svydesign(id = ~群号, weights = ~pw, data = agclus, fpc= ~fpc)
summary(dclus)
#均值估计与标准误差
svymean(~振幅,dclus)
svymean(~总手,dclus)
svymean(~金额,dclus)
m1 <- aggregate(c$振幅, by=list(type=c$群号),mean)
var(m1$x)
(1-5/91)*var(m1$x)/5
m2 <- aggregate(c$总手, by=list(type=c$群号),mean)
var(m2$x)
(1-5/91)*var(m2$x)/5
m3 <- aggregate(c$金额, by=list(type=c$群号),mean)
var(m3$x)
(1-5/91)*var(m3$x)/5

svytotal(~振幅,dclus)
svytotal(~总手,dclus)
svytotal(~金额,dclus)