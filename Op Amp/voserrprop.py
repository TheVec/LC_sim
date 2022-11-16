# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:03:02 2022

@author: Thierry
"""

import math as m
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class Derivatives:
    def __init__(self,f,params,name):
        self.f = sp.simplify(f)
        self.derivs =  list()
        for i in params:
            self.derivs.append(sp.simplify(sp.diff(f,i)))
        self.name = name


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


plt.rcParams['font.size'] = '15'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 

#---------------------------------------------------------------------
#Gain Cheese
gainParams = ['R_1','R_2']
for i in range(0,len(gainParams)):
    gainParams[i] = sp.Symbol(gainParams[i])
    
R2_measured = 978700 #Ohms
R2_rating   = 1000000#Ohms
params = sp.Array(gainParams)

gain = sp.Function('gain_func', real = True)
gain = 1+params[1]/params[0]

R1_measured_OP1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_1offset.txt', usecols = [1], skiprows = 1)
R1_rating_OP1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_1offset.txt', usecols=[2], skiprows = 1)
R1_measured_OP2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_2offset.txt', usecols = [1], skiprows = 1)
R1_rating_OP2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_2offset.txt', usecols = [2], skiprows = 1)

A_OP1_meas = np.zeros((len(params),len(R1_measured_OP1)))
A_OP1_meas[0] = R1_measured_OP1
A_OP1_meas[1].fill(R2_measured)
                 
A_OP1_theo = np.zeros((len(params),len(R1_measured_OP1)))
A_OP1_theo[0] = R1_rating_OP1
A_OP1_theo[1].fill(R2_rating)

err_OP1_meas = np.zeros((len(params),len(R1_measured_OP1)))
err_OP1_meas[0] = R1_measured_OP1/100
err_OP1_meas[1].fill(R2_measured/100)

err_OP1_theo = np.zeros((len(params),len(R1_measured_OP1)))
err_OP1_theo[0] = R1_rating_OP1/20
err_OP1_theo[1].fill(R2_rating/20)


A_OP2_meas = np.zeros((len(params),len(R1_measured_OP1)))
A_OP2_meas[0] = R1_measured_OP2
A_OP2_meas[1].fill(R2_measured)
                 
A_OP2_theo = np.zeros((len(params),len(R1_measured_OP1)))
A_OP2_theo[0] = R1_rating_OP2
A_OP2_theo[1].fill(R2_rating)

err_OP2_meas = np.zeros((len(params),len(R1_measured_OP1)))
err_OP2_meas[0] = R1_measured_OP2/100
err_OP2_meas[1].fill(R2_measured/100)

err_OP2_theo = np.zeros((len(params),len(R1_measured_OP1)))
err_OP2_theo[0] = R1_rating_OP2/20
err_OP2_theo[1].fill(R2_rating/20)

OP1_meas, OP1_meas_err, OP1_name = ErrorProp(gain,params,err_OP1_meas,A_OP1_meas,'Gain first OP07EZ (measured Resistors)')
OP1_theo, OP1_theo_err, OP1_name = ErrorProp(gain,params,err_OP1_theo,A_OP1_theo,'Gain first OP07EZ (theoretical Resistors)')

OP2_meas, OP2_meas_err, OP2_name = ErrorProp(gain,params,err_OP2_meas,A_OP2_meas,'Gain second OP07EZ (measured Resistors)')
OP2_theo, OP2_theo_err, OP2_name = ErrorProp(gain,params,err_OP1_theo,A_OP1_theo,'Gain second OP07EZ (theoretical Resistors)')



R1_measured_lm = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\lm307_offset.txt', usecols = [1], skiprows = 1)
R1_rating_lm = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\lm307_offset.txt', usecols=[2], skiprows = 1)

A_lm_meas = np.zeros((len(params),len(R1_measured_lm)))
A_lm_meas[0] = R1_measured_lm
A_lm_meas[1].fill(R2_measured)

A_lm_theo = np.zeros((len(params),len(R1_measured_lm)))
A_lm_theo[0] = R1_rating_lm
A_lm_theo[1] = R2_rating

err_lm_meas = np.zeros((len(params),len(R1_measured_lm)))
err_lm_meas[0] = R1_measured_lm/100
err_lm_meas[1].fill(R2_measured/100)

err_lm_theo = np.zeros((len(params),len(R1_measured_lm)))
err_lm_theo[0] = R1_rating_lm/20
err_lm_theo[1].fill(R2_rating/20)

LM_meas, LM_meas_err, LM_name = ErrorProp(gain,params,err_lm_meas,A_lm_meas,'Gain of LM307')
LM_theo, LM_theo_err, LM_name = ErrorProp(gain,params,err_lm_theo,A_lm_theo,'Gain of LM307')



R1_measured_tl = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\tl071_offsetx.txt', usecols = [1], skiprows = 1)
R1_rating_tl = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\tl071_offsetx.txt', usecols = [2], skiprows = 1)

A_tl_meas = np.zeros((len(params),len(R1_measured_tl)))
A_tl_meas[0] = R1_measured_tl
A_tl_meas[1].fill(R2_measured)

A_tl_theo = np.zeros((len(params),len(R1_measured_tl)))
A_tl_theo[0] = R1_rating_tl
A_tl_theo[1].fill(R2_rating)

err_tl_meas = np.zeros((len(params),len(R1_measured_tl)))
err_tl_meas[0] = R1_measured_tl/100
err_tl_meas[1].fill(R2_measured/100)

err_tl_theo = np.zeros((len(params),len(R1_measured_tl)))
err_tl_theo[0] = R1_rating_tl/20
err_tl_theo[1].fill(R2_rating/20)

TL_meas, TL_meas_err, TL_name = ErrorProp(gain,params,err_tl_meas,A_tl_meas,'Gain of TL071')
TL_theo, TL_theo_err, TL_name = ErrorProp(gain,params,err_tl_theo,A_tl_theo,'Gain of TL071')

#---------------------------------------------------------------------
#Offset Voltage
Vos_params = ['V_{out}','G']
for i in range(0,len(Vos_params)):
    Vos_params[i] = sp.Symbol(Vos_params[i])

offsetParams = sp.Array(Vos_params)

V_os_f = sp.Function('V_os_f', real = True)
V_os_f = offsetParams[0]/offsetParams[1]

V_out_op1 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_1offset.txt', usecols = [0], skiprows = 1)
V_out_op2 = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\op07_2offset.txt', usecols = [0], skiprows = 1)
V_out_lm = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\lm307_offset.txt', usecols = [0], skiprows = 1)
V_out_tl = np.loadtxt(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\Data\Offset\tl071_offsetx.txt', usecols = [0], skiprows = 1)

A_VOP1_meas = np.zeros((len(Vos_params),len(V_out_op1)))
A_VOP1_meas[0] = V_out_op1
A_VOP1_meas[1] = OP1_meas

A_VOP1_theo = np.zeros((len(Vos_params),len(V_out_op1)))
A_VOP1_theo[0] = V_out_op1
A_VOP1_theo[1] = OP1_theo

A_VOP2_meas = np.zeros((len(Vos_params),len(V_out_op2)))
A_VOP2_meas[0] = V_out_op2
A_VOP2_meas[1] = OP2_meas

A_VOP2_theo = np.zeros((len(Vos_params),len(V_out_op2)))
A_VOP2_theo[0] = V_out_op2
A_VOP2_theo[1] = OP2_theo

A_VLM_meas = np.zeros((len(Vos_params),len(V_out_lm)))
A_VLM_meas[0] = V_out_lm
A_VLM_meas[1] = LM_meas

A_VLM_theo = np.zeros((len(Vos_params),len(V_out_lm)))
A_VLM_theo[0] = V_out_lm
A_VLM_theo[1] = LM_theo

A_VTL_meas = np.zeros((len(Vos_params),len(V_out_tl)))
A_VTL_meas[0] = V_out_tl
A_VTL_meas[1] = TL_meas

A_VTL_theo = np.zeros((len(Vos_params),len(V_out_tl)))
A_VTL_theo[0] = V_out_tl
A_VTL_theo[1] = TL_theo

err_VOP1_meas = np.zeros((len(Vos_params),len(V_out_op1)))
err_VOP1_meas[0].fill(0.1) #Subject to change
err_VOP1_meas[1] = OP1_meas_err

err_VOP1_theo = np.zeros((len(Vos_params),len(V_out_op1)))
err_VOP1_theo[0].fill(0.1) #Subject to change
err_VOP1_theo[1] = OP1_theo_err

err_VOP2_meas = np.zeros((len(Vos_params),len(V_out_op2)))
err_VOP2_meas[0].fill(0.1) #Subject to change
err_VOP2_meas[1] = OP2_meas_err

err_VOP2_theo = np.zeros((len(Vos_params),len(V_out_op2)))
err_VOP2_theo[0].fill(0.1) #Subject to change
err_VOP2_theo[1] = OP2_theo_err

err_VLM_meas = np.zeros((len(Vos_params),len(V_out_lm)))
err_VLM_meas[0].fill(0.1) #Subject to change
err_VLM_meas[1] = LM_meas_err

err_VLM_theo = np.zeros((len(Vos_params),len(V_out_lm)))
err_VLM_theo[0].fill(0.1) #Subject to change
err_VLM_theo[1] = LM_theo_err

err_VTL_meas = np.zeros((len(Vos_params),len(V_out_tl)))
err_VTL_meas[0].fill(0.1) #Subject to change
err_VTL_meas[1] = TL_meas_err

err_VTL_theo = np.zeros((len(Vos_params),len(V_out_tl)))
err_VTL_theo[0].fill(0.1) #Subject to change
err_VTL_theo[1] = TL_theo_err

Vos_OP1m, Vos_OPm1_err, Vos_OP1m_n = ErrorProp(V_os_f, offsetParams, err_VOP1_meas, A_VOP1_meas, 'Offset1')
Vos_OP1t, Vos_OPt1_err, Vos_OP1t_n = ErrorProp(V_os_f, offsetParams, err_VOP1_theo, A_VOP1_theo, 'Offset2')
Vos_OP2m, Vos_OPm2_err, Vos_OP2m_n = ErrorProp(V_os_f, offsetParams, err_VOP2_meas, A_VOP2_meas, 'Offset3')
Vos_OP2t, Vos_OPt2_err, Vos_OP2t_n = ErrorProp(V_os_f, offsetParams, err_VOP2_theo, A_VOP2_theo, 'Offset4')

Vos_LMm, Vos_LMm_err, Vos_LMm_n = ErrorProp(V_os_f, offsetParams, err_VLM_meas, A_VLM_meas, 'Offset5')
Vos_LMt, Vos_LMt_err, Vos_LMt_n = ErrorProp(V_os_f, offsetParams, err_VLM_theo, A_VLM_theo, 'Offset6')

Vos_TLm, Vos_TLm_err, Vos_TLm_n = ErrorProp(V_os_f, offsetParams, err_VTL_meas, A_VTL_meas, 'Offset7')
Vos_TLt, Vos_TLt_err, Vos_TLt_n = ErrorProp(V_os_f, offsetParams, err_VTL_theo, A_VTL_theo, 'Offset8')

Plot = plt.figure(figsize=(15,10))
plt.grid(True)
plt.errorbar(LM_meas, Vos_LMm, Vos_LMm_err, LM_meas_err, fmt='o',capsize = 5, color = 'gray', markerfacecolor = 'blue')
# plt.errorbar(TL_theo, Vos_TLt, Vos_TLt_err, TL_theo_err, fmt='o',capsize = 5, label = 'Rated values')
plt.title('Input Offset Voltage of LM307', fontsize = 40)
plt.xlabel('Gain', fontsize=30)
plt.ylabel('$V_{OS}$ [mV]', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# plt.legend(fontsize=20)
plt.savefig(r'C:\Users\Thierry\Documents\Uni\Labcourse\Op Amp\power shovel.png')
plt.close(Plot)

#-----------------------------------------------------------------------------------------------------------------------------------
#Averages
OP1_mean = np.mean(Vos_OP1m)
OP1_std = np.std(Vos_OP1m)

OP2_mean = np.mean(Vos_OP2m)
OP2_std = np.std(Vos_OP2m)

TL_mean = np.mean(Vos_TLm)
TL_std = np.std(Vos_TLm)

avg_err_op1 = np.mean(Vos_OPm1_err)
avg_err_op2 = np.mean(Vos_OPm2_err)
avg_err_tl = np.mean(Vos_TLm_err)

print('OP07EZ_1', OP1_mean, '$\pm$', OP1_std)
print('OP07EZ_2', OP2_mean, '$\pm$', OP2_std)
print('TL071CP', TL_mean, '$\pm$', TL_std)
print('------------------------------------------------------------')
print('Average Errors')
print('OP1', avg_err_op1)
print('OP2', avg_err_op2)
print('TL', avg_err_tl)

