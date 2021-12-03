import random,math
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
random.seed(1)
data1 = pd.read_excel('./数据采集数据.xlsx')
data = data1[['振幅','总手','金额','换手率']]
print(data1.shape)
data.head()

#进行简单随机抽样
def simple_sampling(data, n):
    idex = random.sample(range(len(data)), n)
    samples = data.iloc[idex,:].copy()
    return samples

#计算入样样本量
def samp_numb(N,d,alpha,S):
    z = stats.norm.ppf((1-alpha/2),loc=0,scale=1)
    a = 1/N + d**2/(z**2 * S**2)
    n = 1/a
    return n

#计算置信区间
def confidence_interval(mean,var,alpha):
    z = stats.norm.ppf((1-alpha/2),loc=0,scale=1)
    a = mean - math.sqrt(var) * z
    a = round(a,3)
    b = mean + math.sqrt(var) * z
    b = round(b,3)
    return [a,b]

#计算简单随机估计均值的方差
def var_ys(lst):
    std = lst.std(ddof = 1)
    f = n/len(data)
    var = ((1-f)/n) * std**2
    return var

# 定义比率估计均值的方差
def var_yr(R,t_std,s_yx,x_var,n):
    f = n/len(data)
    a = (1-f)/n
    b = t_std**2 - 2*R*s_yx + R**2*x_var
    var = a * b
    return var

#计算回归估计均值的方差
def var_yl(n,s_yx,x_std,t_std):
    f = n/len(data)
    p = s_yx/(x_std*t_std)
    var = ((1-f)/n) * (t_std**2) * (1 - p**2)
    return var
    
# 计算相关系数矩阵
data.corr()

## 可视化数据的相关系数热力图

datacor = np.corrcoef(data.values,rowvar=0)
datacor = pd.DataFrame(data=datacor,columns=[data.columns],
                       index=data.columns)
plt.figure(figsize=(5,4))
ax = sns.heatmap(datacor,square=True,annot=True,fmt = ".3f",
                 linewidths=.5,cmap='rainbow',
                 cbar_kws={"fraction":0.046, "pad":0.03})
ax.set_xlabel('指标')
plt.show()

# 选取'换手率作为辅助变量'来进行比率估计和回归估计
x_mean = data.iloc[:,3].mean()
x_std = data.iloc[:,3].std(ddof=1)
#对辅助变量进行抽样
N = len(data)
r = 0.1
alpha = 0.05
n_x = int(samp_numb(N,(r*x_mean),alpha,x_std)) + 1
print('辅助变量换手率的抽取样本量 n/N:',n_x ,'/',N)
samples_x = simple_sampling(data, n_x)
xs_mean = samples_x.iloc[:,3].astype(np.float32).mean()

for i in range(3):
    t_mean = data.iloc[:,i].astype(np.float32).mean()
    t_std = data.iloc[:,i].astype(np.float32).std(ddof = 1)
    d = r * t_mean
    n = int(samp_numb(N,d,alpha,t_std)) + 1
    print('抽样样本量选择 n/N:',n ,'/',N)
    #进行抽样
    print(f"简单随机抽样第{i}组")
    samples = simple_sampling(data, n)
#     print(samples[:3])

    #1简单随机抽样参数
    s_mean = samples.iloc[:,i].astype(np.float32).mean()
    lst = np.array(samples.iloc[:,i].astype(np.float32))
    s_var = var_ys(lst)
    
    #2比率估计参数
    R_hat = t_mean/x_mean
    s_yx = data.iloc[:,i].cov(data.iloc[:,3])
    r_mean = xs_mean * R_hat
    r_var = var_yr(R_hat,t_std,s_yx,(x_std**2),n_x)

    #3回归估计参数
    b = s_yx/(x_std**2)
    l_mean = t_mean + b*(xs_mean - x_mean)
    l_var = var_yl(n_x,s_yx,x_std,t_std)
    interval1 = confidence_interval(t_mean,(t_std**2),alpha)
    interval2 = confidence_interval(s_mean,s_var,alpha)
    interval3 = confidence_interval(r_mean,r_var,alpha)
    interval4 = confidence_interval(l_mean,l_var,alpha)

    print('1.Total   mean{}:{:.3f}  var{}:{:.9f} interval{}:'.format(i,t_mean,i,(t_std**2)/len(data),interval1))
    print('2.SRS     mean{}:{:.3f}  var{}:{:.9f} interval{}:'.format(i,s_mean,i,s_var,interval2))
    print('3.Ratio:  mean{}:{:.3f}  var{}:{:.9f} interval{}:'.format(i,r_mean,i,r_var,interval3))
    print('4.Regre:  mean{}:{:.3f}  var{}:{:.9f} interval{}:'.format(i,l_mean,i,l_var,interval4))
    print('\n')