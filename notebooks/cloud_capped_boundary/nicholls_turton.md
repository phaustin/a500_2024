---
jupytext:
  cell_metadata_filter: all
  encoding: '# -*- coding: utf-8 -*-'
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

### Move to the full Nicholls-Turton entrainment parameterization, following Gesso et al. 2014

Read in the model result for the simple radiative entrainment closure of de Roode lecture 2 and use those
values to calculate the NT entrainment rate

```{code-cell} ipython3
:trusted: true

import context
from matplotlib import pyplot as plt
from a500.utils.helper_funs import make_tuple
from a500.thermo import thermfuncs as tf
from a500.thermo import thermconst as tc
import pandas as pd
import numpy as np
import pdb

with open('vapor_profile.csv') as f:
    df_result=pd.read_csv(f)
    
with open('dumpradiative.csv') as f:
    df_result=pd.read_csv(f)
out=df_result.plot('time','h')

print(tf.__file__)
```

```{code-cell} ipython3
:trusted: true

df_result.tail()
```

### turn the last timestep values into a named tuple

```{code-cell} ipython3
:trusted: true

out=df_result.iloc[-1]  #final timestep in dataframe
print(out)
steady_state=make_tuple(out.to_dict())
```

### plot the $\theta_l$ and $q_t$  flux profiles at 30 levels

```{code-cell} ipython3
:trusted: true

def flux_prof(z,coeffs):
    Fout=coeffs.Fsfc + (coeffs.Finv - coeffs.Fsfc)*(z/coeffs.zinv)
    return Fout

zvals=np.linspace(0,steady_state.h,30)
coeffs_thetal=make_tuple(dict(Fsfc=steady_state.T_flux_0,Finv=steady_state.entflux_theta,
                       zinv=steady_state.h))
coeffs_qt=make_tuple(dict(Fsfc=steady_state.q_flux_0,Finv=steady_state.entflux_qv,
                       zinv=steady_state.h))
flux_thetal=flux_prof(zvals,coeffs_thetal)
flux_qt=flux_prof(zvals,coeffs_qt)
df_flux=pd.DataFrame.from_records(zip(zvals,flux_thetal,flux_qt),columns=['z','flux_thetal','flux_qt'])


fig,(ax0,ax1) = plt.subplots(1,2,figsize=(12,10))
df_flux.plot('flux_thetal','z',ax=ax0)
out=ax1.plot(flux_qt*2.5e6,zvals)

out=ax0.set(title=r'$\theta_l$ flux (K m/s)',ylabel='height (m)')
ax1.set(title=r'$q_t\ flux\ (W m^{-2})$',ylabel='height (m)');
```

## Now turn this into a buoyancy flux profile

```{code-cell} ipython3
:trusted: true

from a500.thermo.thermfuncs import find_press, calc_ABcoeffs
press_vec = find_press(zvals)
#
# find A and B coefficients at each level
# note that qv = qt and theta=thetal in interactive_vapor.ipynb
#

A_list=[]
B_list=[]
for press0 in press_vec:
    A, B, issat=calc_ABcoeffs(steady_state.theta,steady_state.qv,press0)
    A_list.append(A)
    B_list.append(B)    
    
A=np.array(A_list)
B=np.array(B_list)

    
buoyancy_flux = A*flux_thetal + B*flux_qt
df_flux['buoyancy'] = buoyancy_flux

fig, ax0 = plt.subplots(1,1,figsize=(8,12))
df_flux.plot('buoyancy','z',ax=ax0)
out=ax0.set(title=r'buyouancy flux (K m/s)',ylabel='height (m)')
```

### borrow calc_lcl from interactive_vapor notebook

```{code-cell} ipython3
:trusted: true

def calc_lcl(row,psfc):
    """
      find the lcl (in m) for a row in the dataframe
    """
    Tdew = tf.tmr(row['qv'],psfc)
    LCL = tf.LCL(Tdew,row['theta'],psfc)  #kPa
    #
    # rough approximation:  10 kPa = 1 km
    #
    delp=psfc - LCL
    lcl_z= delp*100.
    #pdb.set_trace()
    return lcl_z, LCL

lcl_z, lcl_p = calc_lcl(df_result.iloc[-1],100.)
lcl_z, lcl_p
```

### calculate the saturated and unsaturated thetav jumps at the inversion

(unnumbered del Gesso equations below equation 14)

```{code-cell} ipython3
:trusted: true

dth=steady_state.deltheta
dqt=steady_state.delqv
thetal_m=steady_state.theta
qt_m=steady_state.qv
h=steady_state.h
press=tf.find_press(steady_state.h)   #kPa
thetal_ft = steady_state.theta + dth
qt_ft = steady_state.qv + dqt

Ad,Bd,issat = tf.calc_ABcoeffs(thetal_ft,qt_ft,press)
Aw,Bw,issat = tf.calc_ABcoeffs(thetal_m,qt_m,press)
invert= tf.t_uos_thetal(thetal_m,qt_m,press)
T_0 = invert.temp
lv=tf.L_t(invert.temp)
Cl =  (Ad*lv/tc.CPD - T_0/tc.EPS)
del_thv_dry = Ad * dth + Bd * dqt
del_thv_sat = Aw * dth + Bw * dqt
print('del_thv_dry',del_thv_dry)
print('del_thv_sat',del_thv_sat)
```

```{code-cell} ipython3
:trusted: true

Aw, Bw
```

###  calculate the thetav inversion jump accounting for evaporative cooling

(see Stevens 2002 equations 16-18)

```{code-cell} ipython3
:trusted: true

ql_max = invert.ql
print('ql_max at cloud top (kg/kg)',ql_max)
Cl =  (Ad*lv/tc.CPD - T_0/tc.EPS)
Del_thv = del_thv_dry - Cl * ql_max
print('Del_thv',Del_thv)
```

### calculate the buoyancy integral terms

Gesso equations 13-14

```{code-cell} ipython3
:trusted: true

zi = steady_state.h
lcl_press=tf.LCL_thetal(thetal_m,qt_m)
zb=tf.find_height(lcl_press)

T1 = zb/zi
T2 = 0.5 * zb**2 / zi**2
T3 = (zi-zb)/zi
T4 = 0.5 * (zi**2 - zb**2) / zi**2

wtl_0=steady_state.T_flux_0
wqt_0=steady_state.q_flux_0
Del_F = steady_state.radcool/tc.CPD

term1 = wtl_0 * (Ad * (T1-T2) + Aw * (T3-T4))
term2 = wqt_0 * (Bd * (T1-T2) + Bw * (T3-T4))
term3 = Del_F * (Ad * T2      + Aw * T4)

Theta_NE = term1 + term2 + term3
print('Gesso Θne',Theta_NE)
print(zb)
```

Find wstar using Gesso equations 8 and 12

```{code-cell} ipython3
:trusted: true

wstar=(2.5*9.8/T_0*zi*Theta_NE)**(1/3.)
print('wstar without entrainment: {:5.3f} (m/s)'.format(wstar))
```

### Calculate the densest mixture for this inversion jump

Stevens equation 20

```{code-cell} ipython3
:trusted: true

chi_star = Cl * ql_max / (del_thv_dry - del_thv_sat)
print('just saturated at with {:5.2f}% environmental air'.format(chi_star*100.))
```

### Calculate the Nicholls and Turton average evaporative cooling effect $\Delta m / \Delta \theta_v$

Stevens eq. 30 and de Roode lecture 2  slide 12 -- note that $\Delta m/\Delta \theta_v = 1$ for no evaporation

```{code-cell} ipython3
:trusted: true

Del_m = del_thv_dry + chi_star * (2. - chi_star) * (del_thv_sat - del_thv_dry)
print('Δm/Δθv = {:5.2f}'.format(Del_m/Del_thv))
```

### Calculate the weakened Nicholls and Turton inversion buoyancy jump

de Roode lecture 2 slide 15 and Stevens eqn 29 with a2=15 following Bretherton

```{code-cell} ipython3
:trusted: true

a2=15.
Del_thv_NT = Del_thv / (1. + a2 * (1. - Del_m/Del_thv))
print('original Del_thv={:5.2f} (K), Del_thv_NT = {:5.2f} (K)'.format(Del_thv,Del_thv_NT))
```

### Calculate the final entrainment rate according to de Roode lecture 2 slide 15

```{code-cell} ipython3
:trusted: true

A_NT = 0.2
fac_NT = 2.5

term4 = Del_thv_NT
term5 = A_NT * fac_NT * (T2 * del_thv_dry + T4 * del_thv_sat)
denominator = term4 + term5

we = A_NT * fac_NT * Theta_NE / denominator
print('radiative we is {:5.3f} cm/s and NT we is {:5.3f} cm/s'.format(steady_state.went*100.,we*100.))
```

```{code-cell} ipython3
:trusted: true


```
