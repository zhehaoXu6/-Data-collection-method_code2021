setwd(dir =" C:\Users\wangj\Desktop")

install.packages("sampling")
install.packages("survey")
library(grid)
library("sampling")
library(survey)
set.seed(123)
data <- read.csv("600519.csv")
a =rep(1:91,each = 8 )
b = 1:728
data1 = data.frame("群号"= a,"时间" = b)
data = cbind(data,data1)
#进行整群抽样
sampling:::cluster(data,clustername="群号",size=25,method="srswor",description=TRUE)

m = sampling:::cluster(data,clustername="群号",size=25,method="srswor",description=TRUE)
m = getdata(data, m)
result = unique(m$群号)
cat("Clusters selected in stage 1:",result)

sm = NULL
for(i in 1:25)
{mi = m[m$"群号" == result[i],]
l = nrow(mi)
ni = round(l/5)
si = srswor(ni,l)
si = mi[si!= 0,]
sm = rbind(sm,si)
}
#估计
#fpc1是总体中的群的个数
fpc1 = rep(50, nrow(sm))
#fpc2是每个群中的id的个数
fpc2 = rep(8,nrow(sm))
sm = as.data.frame(cbind(sm,fpc1,fpc2))
dsm <- svydesign(id = ~群号+群号,fpc= fpc1+fpc2,data = sm)
summary(dsm)

svymean(~振幅,dsm)
svymean(~总手,dsm)
svymean(~金额,dsm)
svyvar(~振幅,dsm)
svyvar(~总手,dsm)
svyvar(~金额,dsm)

svytotal(~振幅,dsm)
svytotal(~总手,dsm)
svytotal(~金额,dsm)


