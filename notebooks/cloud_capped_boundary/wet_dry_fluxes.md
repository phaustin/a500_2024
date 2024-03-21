---
jupytext:
  cell_metadata_filter: all
  cell_metadata_json: true
  notebook_metadata_filter: all,-language_info
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
latex_envs:
  LaTeX_envs_menu_present: true
  autoclose: false
  autocomplete: true
  bibliofile: biblio.bib
  cite_by: apalike
  current_citInitial: 1
  eqLabelWithNumbers: true
  eqNumInitial: 1
  hotkeys:
    equation: meta-9
  labels_anchors: false
  latex_user_defs: false
  report_style_numbering: false
  user_envs_cfg: false
toc:
  base_numbering: 1
  nav_menu: {}
  number_sections: true
  sideBar: false
  skip_h1_title: false
  title_cell: Table of Contents
  title_sidebar: Contents
  toc_cell: true
  toc_position: {}
  toc_section_display: block
  toc_window_display: false
---

+++ {"toc": true}

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#buoyancy-flux-in-a-cloudy-boundary-layer" data-toc-modified-id="buoyancy-flux-in-a-cloudy-boundary-layer-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>buoyancy flux in a cloudy boundary layer</a></span></li></ul></div>

```{code-cell} ipython3
:scrolled: true
:trusted: true

print("start")
import context

from pathlib import Path
import sys
import a500
print(f'imported {a500.__path__[0]}')
```

# buoyancy flux in a cloudy boundary layer

+++

We want to find $A_w, B_w, A_d$ and $B_d$ such that out of cloud:

$$\overline{w^\prime\theta_v^\prime}=A_d\overline{w^\prime\theta_l^\prime}+B_d\overline{w^\prime q_v^\prime}$$

while in cloud:



$$\overline{w^\prime\theta_v^\prime}=A_w\overline{w^\prime\theta_l^\prime}+B_w\overline{w^\prime q_t^\prime}$$


where $A_d=1+0.61\overline{q_v}$ and $B_d=0.61\overline{\theta}$,

and

$$\begin{aligned}
&A_w=\frac{1+\frac{\overline{q_s}}{\epsilon}-\overline{q_t}+\frac{\overline{\theta}}{\epsilon}\left(\frac{dq_s}{dT}\right)}{1+\frac{L_v}{c_p}\left(\frac{dq_s}{dT}\right)},\\[2mm]
&B_w=A_w\left(\frac{L_v}{c_p}\right)-\overline{\theta}.
\end{aligned}\\[5mm]$$

+++

- Use de Roode equations 5.18,  5.29 and 5.30 to evaluate $A_d$, $B_d$, $A_w$ and $B_w$ at a pressure of 900 hPa, temperature of 280 K, $q_s$ = 7 g/kg, $L_v$ = $2.485 \times 10^{6}$ J/kg, $R_v$ = 461.5 J/kg/K, $q_v$ = $q_s$.

- Assuming a surface pressure of 100. kPa, Tsurf=290. K and qvap=7.e-3 kg/kg, find cloud base and
  plot the vertical profile of cloud liquid water, assume total water and $\theta_l$ remain constant with height.

```{code-cell} ipython3
:trusted: true

def calc_w(theta, qv, press):
    """
    Parameters
    ----------
    
    theta: float
       potential temperature (K)
    
    qv: float
       saturation mixing ratio (kg/kg)
       
    press: float
       pressure (kPa)
       
    Returns
    -------
    
    Aw, Bw: (floats)
       buoyancy flux coefficients assuming saturation
       
    """
    epsilon_i = 0.61
    epsilon = 1/(1 + epsilon_i)
    P0 = 100 # kPa
    T = theta/((P0/press)**(0.286))
    Lv = 2.485e6
    Rv = 461.5
    cp = 1004
    dqdt = (qv*Lv)/(Rv*T**2)
    Aw = (1 + qv/epsilon - qv + theta/epsilon*dqdt)/(1+Lv/cp*dqdt)
    Bw = Aw*(Lv/cp) - theta
    return Aw,Bw

def calc_d(theta, qv):
    """
    Parameters
    ----------
    
    theta: float
       potential temperature (K)
    
    qv: float
       saturation mixing ratio (kg/kg)
       
    Returns
    -------
    
    Ad, Bd: (floats)
       buoyancy flux coefficients assuming subsaturation
    """
    
    epsilon_i = 0.61
    Ad = 1 + epsilon_i*qv
    Bd = epsilon_i*theta
    return Ad,Bd


from a500.thermo.thermfuncs import find_theta, find_rs
press=90.  #kPa
Temp = 280. #K
theta = find_theta(Temp,press)
qv = find_rs(Temp,press)
print(f"dry A and B are {calc_d(theta,qv)}")
print(f"saturated A and B are {calc_w(theta,qv,press)}")
```

```{code-cell} ipython3
:trusted: true

import numpy as np

from a500.thermo import thermfuncs as tf
import pandas as pd

Temp=280. #K
press=90. #kPa
#
# find the saturation mixing ratio and potential temp from the temperature and pressure
#
print(tf.qs_tp(Temp,press))
print(tf.find_theta(Temp,press))
#
# find the dew point temperature and the lifting condensation level
#
psurf=100.  #kPa
Tsurf=290.
qvap=7.e-3  #kg/kg
Tdew = tf.tmr(qvap,psurf)
print('the surface dew point temp is: ',Tdew)
LCL = tf.LCL(Tdew,Tsurf,psurf)
print('the LCL is {:5.2f} kPa'.format(LCL))

#
# find thetal 
#
thetal = tf.alt_thetal(psurf,Tsurf,qvap)
#
# invert thetal for temperature, vapor, liquid -- uos means "unsaturated or saturated"
#
print(tf.t_uos_thetal(thetal,qvap,80.))
#
# make a sounding
#
press_levs=np.linspace(80,100.,20.)
press_levs=press_levs[::-1]
sounding=[]
for press in press_levs:
    sounding.append(tf.t_uos_thetal(thetal,qvap,press))
    
df_sounding=pd.DataFrame.from_records(sounding,columns=["temp","ql","issat","qv"])
df_sounding.tail()
```

```{code-cell} ipython3
:trusted: true

from matplotlib import pyplot as plt
fig,(ax0,ax1) = plt.subplots(1,2,figsize=(12,8))
ax0.plot(df_sounding['qv']*1.e3,press_levs)
ax0.invert_yaxis()
ax1.plot(df_sounding['ql']*1.e3,press_levs)
ax1.invert_yaxis()
ax0.set(title='vapor mixing ratio',xlabel='qv (g/kg)',ylabel='pressure (kPa)')
ax1.set(title='liquid mixing ratio',xlabel='ql (g/kg)',ylabel='pressure (kPa)')
plt.show()
```

```{code-cell} ipython3
:trusted: true


```
