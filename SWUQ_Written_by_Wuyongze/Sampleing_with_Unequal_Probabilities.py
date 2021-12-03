import numpy as np
import pandas as pd

np.random.seed(9984)
lamda = 10000000

#z是辅助变量(需要归一化)，y是采样样本集合,
#案例中不等概抽样的psu单元为每一天的数据结果,4是辅助变量
data = pd.read_excel('600519.xlsx',
                     sheet_name='Sheet1',usecols=[1,2,3,4])
data = data.drop(index=data[data['金额'] == '--'].index)
#print(data['总手']) y:振幅 总手 金额  z:换手%
z_data = data['换手率']
y_data = data['金额']

#z辅助变量归一化
z_data = z_data/np.sum(z_data)

z_data = np.array(z_data)
y_data = np.array(y_data)
z_data.astype('float')
y_data.astype('float')
z = z_data

#代码法
def daima(z):
    rd_1 = np.random.uniform(low=0.0, high=np.sum(z))
    z_sum = np.zeros(len(z))
    z_sum[0] = z[0]
    first = 0
    for i in range(1,len(z)):
        z_sum[i] = z[i]+z_sum[i-1]
    for i in range(len(z)):
        if i == 0 and rd_1<z_sum[i]:
            first = i
            break
        if i >0:
            if rd_1>z_sum[i-1] and rd_1<=z_sum[i]:
                first = i
                break
    #first这是下标，需要加1
    first_item = z[first]
    return first,first_item

#拉希里法
def laxili(z):
    id_num = len(z)
    id_get = -1
    while id_get == -1:
        rd_m = np.random.uniform(low=0, high=np.max(z))
        rd_id = np.random.randint(low=0, high=len(z))
        if z[rd_id]>=rd_m and z[rd_id]!=0:
            id_get = rd_id
            break
    #id_get这是下标，需要加1
    id_item = z[id_get]
    return id_get,id_item

#可放回抽样-代码法
def PPS_daima(z,n):
    z = np.array(z)
    z = z*lamda
    out = np.zeros(n)
    out.astype('int')
    out = list(out)
    for i in range(n):
        out[i] = daima(z)[0]
    return out

#可放回抽样-拉希里法
def PPS_laxili(z,n):
    z = np.array(z)
    z = z*lamda
    out = np.zeros(n)
    out.astype('int')
    out = list(out)
    for i in range(n):
        out[i] = laxili(z)[0]
    return out

#不放回抽样，Yates-Grundy-代码法
def Y_G_daima(z,n):
    z = np.array(z)
    z = z*lamda
    first,first_item = daima(z)
    zii = lamda
    out = np.zeros(n)
    out.astype('int')
    out_id,out_item = first,first_item
    out = list(out)
    out[0] = out_id
    for i in range(n-1):
        zii = zii-z[out_id]
        z[out[i]] = 0
        z_new = z/zii
        out_id,out_item = daima(z_new)
        out[i+1] = out_id
    out = np.array(out)
#    out = out+1
    return out

#不放回抽样，Yates-Grundy-拉希里法
def Y_G_laxili(z,n):
    z = np.array(z)
    z = z*lamda
    first,first_item = laxili(z)
    zii = lamda
    out = np.zeros(n)
    out.astype('int')
    out_id,out_item = first,first_item
    out = list(out)
    out[0] = out_id
    for i in range(n - 1):
        zii = zii - z[out_id]
        z[out[i]] = 0
        z_new = z / zii
        out_id, out_item = laxili(z_new)
        out[i + 1] = out_id
    out = np.array(out)
#    out = out+1
    return out

#估计piPS-Yates方法下的总体总值/均值/总值方差/均值方差
def Raj(id,z,y):
    n = len(id)
    t = np.zeros(n)
    t[0] = y[id[0]]/z[id[0]]
    for i in range(1,n):
        t[i] = np.sum(y[id[0:i-1]])+y[id[i]]/z[id[i]]*\
               (1-np.sum(z[id[0:i-1]]))
    Y_raj = np.mean(t)
    v_Y_raj = 1/(n*(n-1))*np.sum((t-Y_raj)**2)
    Yu_raj = Y_raj/len(y)
    v_Yu_raj = v_Y_raj/(len(y)**2)
    return Y_raj,v_Y_raj,Yu_raj,v_Yu_raj

#估计PPS方法下的总体总值/均值/总值方差/均值方差
def HH(id,z,y):
    n = len(id)
    Y_hh = 1/n*np.sum(y[id[:]]/z[id[:]])
    v_Y_hh = 1/(n*(n-1))*np.sum((y[id[:]]/z[id[:]]-Y_hh)**2)
    Yu_hh = Y_hh/len(y)
    v_Yu_hh = v_Y_hh/(len(y)**2)
    return Y_hh,v_Y_hh,Yu_hh,v_Yu_hh


print('y_sum:',np.sum(y_data),'y_u:',np.mean(y_data),'\n')
#PPS代码法抽样
pps_daima_id = PPS_daima(z,100)
Y,v_Y,Yu,v_Yu = HH(pps_daima_id,z_data,y_data)
print('PPS代码法')
print('估计：y_sum',Y,'估计方差：y_sum_var',v_Y,
      '估计：y_u',Yu,'估计方差：y_u_var',v_Yu)
print('估计y_u的偏差：',(Yu-np.mean(y_data))/np.mean(y_data))
#PPS拉希里法抽样
pps_laxili_id = PPS_laxili(z,100)
Y,v_Y,Yu,v_Yu = HH(pps_laxili_id,z_data,y_data)
print('PPS拉希里法')
print('估计：y_sum',Y,'估计方差：y_sum_var',v_Y,
      '估计：y_u',Yu,'估计方差：y_u_var',v_Yu)
print('估计y_u的偏差：',(Yu-np.mean(y_data))/np.mean(y_data))
#Y_G_代码法抽样
yates_daima_id = Y_G_daima(z,100)
Y,v_Y,Yu,v_Yu = Raj(yates_daima_id,z_data,y_data)
print('Y_G 代码法')
print('估计：y_sum',Y,'估计方差：y_sum_var',v_Y,
      '估计：y_u',Yu,'估计方差：y_u_var',v_Yu)
print('估计y_u的偏差：',(Yu-np.mean(y_data))/np.mean(y_data))
#Y_G_拉希里法抽样
yates_laxili_id = Y_G_laxili(z,100)
Y,v_Y,Yu,v_Yu = Raj(yates_laxili_id,z_data,y_data)
print('Y_G 拉希里法')
print('估计：y_sum',Y,'估计方差：y_sum_var',v_Y,
      '估计：y_u',Yu,'估计方差：y_u_var',v_Yu)
print('估计y_u的偏差：',(Yu-np.mean(y_data))/np.mean(y_data))