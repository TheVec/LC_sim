# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:53:27 2022

@author: Thierry
"""

import math as m
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt


plt.rcParams['font.size'] = '15'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 

class Derivatives:
    def __init__(self,f,params,name):
        self.f = sp.simplify(f)
        self.derivs =  list()
        for i in params:
            self.derivs.append(sp.simplify(sp.diff(f,i)))
        self.name = name

def LinReg(dataX,dataY,err):
    A = np.zeros((len(dataX),2))
    for i in range(0,len(dataX)):
        A[i][0] = 1
        for j in range(1,2):
            A[i][j] = dataX[i]**j
    P = np.zeros((len(dataX),len(dataX)))
    for i in range(0,len(dataX)):
        for j in range(0,len(dataX)):
            if i == j:
                P[i][j]=1/(err[i])**2
    
    x = np.linalg.inv(np.transpose(A)@P@A)@(np.transpose(A)@P@(dataY))
    fitData = A@x
    err = np.linalg.inv(np.transpose(A)@P@A)
    return x, fitData, np.sqrt(np.diag(err))

def ErrorProp(Func,Params,err_val,DataArray,name):
    #Initialise Class, named f
    f = sp.Function('f', real=True)
    f = Derivatives(Func,Params,name)
    print('Function ' + name + ':', f.f)
    print('Derivatives of '+name+' (in order of Params): ', f.derivs)
    
    #Errorformula
    fError = 0
    ErrorList = list()
    for i in range(len(Params)):
        ErrorList.append('s_'+str(Params[i]))
        ErrorList[i] = sp.Symbol(ErrorList[i])
        fError = fError + f.derivs[i]**2 * ErrorList[i]**2
    sp.simplify(fError)
    fError = sp.sqrt(fError)
    print('Error Formula '+name+':', fError)

    
    #Evaluate Data
    results = list()
    errors = list()
    for i in range(0,np.size(DataArray,1)):
        helpf = f.f
        helpd = fError
        for j in range(0,len(Params)):
            helpf = helpf.subs(Params[j],DataArray[j][i])
            helpd = helpd.subs(ErrorList[j],err_val[j][i])
            helpd = helpd.subs(Params[j],DataArray[j][i])
        results.append(float(sp.N(helpf)))
        errors.append(float(sp.N(helpd)))
        print(float(sp.N(helpf)))
    
    print('Function Results with errors, '+name+':')
    for i in range(len(results)):
        print(results[i],r'$/pm$',errors[i])
    
    print('\nFunction ' + name + ' as latex code:', sp.printing.latex(f.f))
    print('Error Formula of '+name+' as latex code:', sp.printing.latex(fError),'\n')
    return results,errors,f.name

R1 = 4638
R2 = 4610
R3 = 9880
R4 = 10.14

freq_sim = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_5V.txt', usecols =[0], skiprows = 1)
Vs1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_5V.txt', usecols =[1], skiprows = 1)
Vx1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_5V.txt', usecols =[2], skiprows = 1)
Vo1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_5V.txt', usecols =[3], skiprows = 1)
Vs2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_8.5V.txt', usecols =[1], skiprows = 1)
Vx2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_8.5V.txt', usecols =[2], skiprows = 1)
Vo2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRR_OLG_8.5V.txt', usecols =[3], skiprows = 1)



VD1 = np.multiply(Vx1, (R4 / (R2 + R4)))
VD2 = np.multiply(Vx2, (R4 / (R2 + R4)))

CMR_sim = 20.0 * np.log10((Vs2-Vs1)/(VD2-VD1))
AOL_sim = 20.0 * np.log10((Vo1-Vo2)/(VD1-VD2))

V_x1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRRDATA.txt', usecols=[1], skiprows=1)
V_x2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRRDATA.txt', usecols=[2], skiprows=1)


FuncParams_Vxi = ['R_3','R_4','V_x']
for i in range(0, len(FuncParams_Vxi)):
    FuncParams_Vxi[i]= sp.Symbol(FuncParams_Vxi[i])

params_Vxi = sp.Array(FuncParams_Vxi)

Vx_func = sp.Function('Vx_func', real = True)
Vx_func = params_Vxi[2]*params_Vxi[1]/(params_Vxi[0]+params_Vxi[1])

A_Vx1 = np.zeros((len(FuncParams_Vxi),len(V_x1)))
A_Vx1[0].fill(R3)
A_Vx1[1].fill(R4)
A_Vx1[2] = V_x1 

A_Vx2 = np.zeros((len(FuncParams_Vxi),len(V_x1)))
A_Vx2[0].fill(R3)
A_Vx2[1].fill(R4)
A_Vx2[2] = V_x2 

err_val_Vx = np.zeros((len(params_Vxi),np.size(A_Vx1,1)))
err_val_Vx[0].fill(float(R3/50)) #Assuming 1% Error
err_val_Vx[1].fill(float(R4/500)) #Assuming .1% Error
err_val_Vx[2].fill(0.01) #This will be changed
0.

V_os1, V_os1_err, V_name1 = ErrorProp(Vx_func,params_Vxi,err_val_Vx,A_Vx1,'V_os1')
V_os2, V_os2_err, V_name2 = ErrorProp(Vx_func,params_Vxi,err_val_Vx,A_Vx2,'V_os2')

#Enter Functionparameters as string: ['s']
FuncParams = ['Vin1','Vin2','Vos1','Vos2']
for i in range(0, len(FuncParams)):
    FuncParams[i]= sp.Symbol(FuncParams[i])

#Transform paramters into something readable for sympy
params = sp.Array(FuncParams)

#Enter Function using array entries or as string: f = params[0]*params[1] or f = 'a * b'
CMR_func = sp.Function('CMR_func', real = True)
CMR_func = 20*sp.log(((params[1]-params[0])/(params[3]-params[2])),10)


#Enter Data, everything in order of paramters in the arrays above
V_in1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRRDATA.txt', usecols=[3], skiprows=1)
V_in2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRRDATA.txt', usecols=[4], skiprows=1)


A_CMR = np.zeros((len(FuncParams),len(V_in1)))
A_CMR[0] = V_in1
A_CMR[1] = V_in2
A_CMR[2] = V_os1
A_CMR[3] = V_os2

err_val_CMR = np.zeros((len(params),np.size(A_CMR,1)))
err_val_CMR[0].fill(0.01) #subject to change
err_val_CMR[1].fill(0.01) #subject to change
err_val_CMR[2] = V_os1_err
err_val_CMR[3] = V_os2_err

#Call function
CMR,sigma_CMR,CMRname = ErrorProp(CMR_func,params,err_val_CMR,A_CMR,'CMR')

# hehe = open(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMR' + CMRname + '.txt','w')
# for i in range(np.size(A_CMR,1)):
#     hehe.write(str(CMR[i])+' ')
#     hehe.write(str(sigma_CMR[i])+'\n')
# hehe.close()

freq = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\CMRRDATA.txt', usecols=[0], skiprows=1)
freq[0] = 1
Plot = plt.figure(figsize=(19,15))
plt.grid(True)
plt.errorbar(np.log10(freq),CMR,sigma_CMR,fmt='o',capsize = 5, label = 'measured data')
plt.plot(np.log10(freq_sim),CMR_sim, label = 'PSpice simulation')
# plt.plot(np.log10(freq),CMR,'o')
plt.title('$CMR = 20\cdot \log_{10}(CMRR)$', fontsize = 45)
plt.xlabel('$\log_{10}(f)$', fontsize=35)
plt.ylabel('CMR [dB]', fontsize=35)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.legend(fontsize=25)
plt.savefig(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\long_reach_excavator.png')
plt.close(Plot)
#---------------------------------------------------------------------------
#Open Loop Gain

V_x1_Aol1 = np.absolute(np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\AolData.txt', usecols=[1], skiprows=1))
V_x2_Aol1 = np.absolute(np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\AolData.txt', usecols=[2], skiprows=1))
V_out1_Aol1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\AolData.txt', usecols=[3], skiprows=1)
V_out2_Aol1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\AolData.txt', usecols=[4], skiprows=1)

A_Vx1_Aol1 = np.zeros((len(FuncParams_Vxi),len(V_x1_Aol1)))
A_Vx1_Aol1[0].fill(R3)
A_Vx1_Aol1[1].fill(R4)
A_Vx1_Aol1[2] = V_x1_Aol1

A_Vx2_Aol1 = np.zeros((len(FuncParams_Vxi),len(V_x1_Aol1)))
A_Vx2_Aol1[0].fill(R3)
A_Vx2_Aol1[1].fill(R4)
A_Vx2_Aol1[2] = V_x2_Aol1 

err_val_Vx_Aol1 = np.zeros((len(params_Vxi),np.size(A_Vx1_Aol1,1)))
err_val_Vx_Aol1[0].fill(float(R3/100)) #Assuming 1% Error
err_val_Vx_Aol1[1].fill(float(R4/1000)) #Assuming .1% Error
err_val_Vx_Aol1[2].fill(0.01) #This will be changed (Error of voltage measurement)

V_os1_Aol1, V_os1_err_Aol1, V_name1_Aol1 = ErrorProp(Vx_func,params_Vxi,err_val_Vx_Aol1,A_Vx1_Aol1,'V_os1_Openloop')
V_os2_Aol1, V_os2_err_Aol1, V_name2_Aol1 = ErrorProp(Vx_func,params_Vxi,err_val_Vx_Aol1,A_Vx2_Aol1,'V_os2_Openloop')

FuncParams_OpenLoop = ['V_{os,1}','V_{os,2}','V_{out,1}', 'V_{out,2}']
for i in range(0,len(FuncParams_OpenLoop)):
    FuncParams_OpenLoop[i] = sp.Symbol(FuncParams_OpenLoop[i])
    
openloop_Params = sp.Array(FuncParams_OpenLoop)

A_OL1 = sp.Function('A_{OL}_Func', real = True)
A_OL1 = 20*sp.log(((openloop_Params[3]-openloop_Params[2])/(openloop_Params[1]-openloop_Params[0])),10)

A_openloop1 = np.zeros((len(FuncParams_OpenLoop),len(V_x1_Aol1)))
A_openloop1[0] = V_os1_Aol1
A_openloop1[1] = V_os2_Aol1
A_openloop1[2] = V_out1_Aol1
A_openloop1[3] = V_out2_Aol1

err_val_Aol1 = np.zeros((len(params),np.size(A_Vx1_Aol1,1)))
err_val_Aol1[0] =  V_os1_err_Aol1
err_val_Aol1[1] =  V_os2_err_Aol1
err_val_Aol1[2].fill(0.01)
err_val_Aol1[3].fill(0.01)

A_openloop1r, A_openloop_err1, A_openloop_name = ErrorProp(A_OL1,openloop_Params,err_val_Aol1,A_openloop1,'Open loop gain first circuit')

# xy = open(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\ ' + A_openloop_name + '.txt','w')
# for i in range(np.size(A_openloop1,1)):
#     xy.write(str(A_openloop1r[i])+' ')
#     xy.write(str(A_openloop_err1[i])+'\n')
# xy.close()

V_in = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\secondcircuitdata.txt', usecols=[1], skiprows=1)
V_out = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\secondcircuitdata.txt', usecols=[2], skiprows=1)

FuncParams_OpenLoop2 = ['V_{in}', 'V_{out}']
for i in range(0,len(FuncParams_OpenLoop2)):
    FuncParams_OpenLoop2[i] = sp.Symbol(FuncParams_OpenLoop2[i])
    
openloop_Params2 = sp.Array(FuncParams_OpenLoop2)

A_OL2 = sp.Function('A_OL2_func', real = True)
A_OL2 = 20*sp.log((openloop_Params2[1]/openloop_Params2[0]),10)

A_openloop2 = np.zeros((2,len(V_in)))
A_openloop2[0] = V_in
A_openloop2[1] = V_out

err_val_Aol2 = np.zeros((2,np.size(A_openloop2,1)))
err_val_Aol2[0].fill(0.01)
err_val_Aol2[1].fill(0.01)

A_openloop2r, A_openloop_err2, A_openloop_name2 = ErrorProp(A_OL2,openloop_Params2,err_val_Aol2,A_openloop2,'second circuit')
# xyz = open(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\ ' + A_openloop_name2 + '.txt','w')
# for i in range(np.size(A_openloop2,1)):
#     xyz.write(str(A_openloop2r[i])+' ')
#     xyz.write(str(A_openloop_err2[i])+'\n')
# xyz.close()

freq1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\AolData.txt', usecols=[0], skiprows=1)
freq1[2]=1
freq2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\secondcircuitdata.txt', usecols=[0], skiprows=1)

#LinReg A_OL
data_x = list()
data_y = list()
freqh = np.sort(freq1)
for i in range(1,len(freq1)+len(freq2)):
    if i < len(freq1):
        data_x.append(freqh[i])
        data_y.append(A_openloop1r[i])
    else:
        data_x.append(freq2[i-len(freq1)])
        data_y.append(A_openloop2r[i-len(freq1)])

data_x_log = np.log10(data_x)

OL_err = np.append(A_openloop_err1, A_openloop_err2)
coeff, fit_dat, covar = LinReg(data_x_log, data_y,OL_err)
print('\n', 'coeff', coeff)
print('\n', 'coeff_errs', covar)


Plot = plt.figure(figsize=(19,15))
plt.grid(True)
plt.errorbar(np.log10(freq1),A_openloop1r,A_openloop_err1,fmt='o',capsize = 5, color = 'blue', label='First Circuit')
plt.errorbar(np.log10(freq2),A_openloop2r,A_openloop_err2,fmt='o',capsize = 5, color = 'red', label='Second Circuit')
plt.plot(data_x_log, fit_dat, label = 'Linear Regression', color = 'gray')
plt.plot([-0.1,7],[np.max(A_openloop1r)-3,np.max(A_openloop1r)-3], color = 'green', label = '-3dB')
plt.plot([-0.1,7],[0,0], color = 'purple', label = 'unity gain')
plt.plot(np.log10(freq_sim),AOL_sim, label = 'PSpice sim')
plt.title('Open Loop Gain', fontsize = 45)
plt.xlabel('$\log_{10}(f)$', fontsize=35)
plt.ylabel('$20\cdot \log_{10}(A)$', fontsize=35)
plt.xlim(-0.1,7)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.legend(fontsize=25)
plt.savefig(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\vibratory_compactor.png')
plt.close(Plot)
print(np.max(A_openloop1r)-3)

cheese = list()
A_cheese = np.append(A_openloop1r,A_openloop2r)
freq_cheese = np.append(freq1,freq2)
for i in range(0,len(OL_err)):
    cheese.append(freq_cheese[i]*10**(A_cheese[i]/20))
plt.plot(freq_cheese, cheese)