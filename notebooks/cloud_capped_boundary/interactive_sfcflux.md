---
jupytext:
  cell_metadata_filter: all
  cell_metadata_json: true
  formats: md:myst,ipynb
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

(add_subsidence)=
# Make the surface flux interactive and add subsidence

+++

In this notebook we keep the boundary layer dry, and add subsidence at the inversion to the height equation.

We also fix the surface temperature and diagnose the surface flux from the temperature difference between the surface and
the mixed layer.  

$$
\begin{align}
  \text{mean temperature: } \frac{d \hat{\theta} }{dt} &=(1 + k) F_0/(h c_p\rho_*)\label{eq:meantheta}\\
\text{inversion height: } \frac{dh }{dt} &= ( k F_0)/(\rho_* c_p \Delta \theta) + w_h \label{eq:hrise}\\
\end{align}
$$

Note that the layer takes about 15 days to equilibrate

```{code-cell} ipython3
:trusted: true

def theta_ft(h,intercept,gamma):
    """
    construct the theta profile in the free troposphere
    """
    theta_top = intercept + h*gamma
    return theta_top

from collections import namedtuple
def make_tuple(tupname,in_dict):
    the_tup = namedtuple(tupname, in_dict.keys())
    the_tup = the_tup(**in_dict)
    return the_tup
```

```{code-cell} ipython3
:trusted: true

import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt
import pandas as pd


def dmixed_vars(the_vars,tstep,coeffs):
    """
      the_vars[0]= thetabar
      the_vars[1] = h
      
      surface flux from drag law with subsidense and diagnosed deltheta
    """
    #print('the_vars: ',the_vars,D,U)
    k=0.2
    #
    # diagnose the jump
    #
    deltheta = theta_ft(the_vars[1],coeffs.intercept,coeffs.gamma) - the_vars[0]
    Cd = 1.e-3  #drag coefficient
    F0 = coeffs.U*Cd*(coeffs.sst - the_vars[0])
    Fint = -k*F0
    went = -Fint/deltheta
    wsubs = -coeffs.D*the_vars[1]
    rho=1.
    cp=1004.
    derivs=np.empty_like(the_vars)
    derivs[0]=(F0 - Fint)/(the_vars[1]*rho) - 0./1004./the_vars[1]
    derivs[1] = went + wsubs
    return derivs
```

```{code-cell} ipython3
:trusted: true

dtout=15.  #minutes
tf=15*24.   #hours
dtout=dtout*60. #seconds
tf=tf*3600. #seconds
sst=310.  #Kelvins
D=5.e-6  #subsidence s-1
U=7  #surface wind speedm/s
intercept = 292 #K
gamma = 6.e-3  #lapse rate K/m
tspan = np.arange(0.,tf,dtout)
vars_init=[288.,400.]  #theta (K), height (m) to start
the_tup=dict(D=D,U=U,sst=sst,intercept=intercept,gamma=gamma)
the_tup=make_tuple('coeffs',the_tup)
output=integrate.odeint(dmixed_vars, vars_init, tspan,(the_tup,))
result=pd.DataFrame.from_records(output,columns=['theta','h'])
result['time']=tspan/3600./24.  #days
result['deltheta'] = theta_ft(result['h'].values,intercept,gamma) - result['theta']
```

```{code-cell} ipython3
:trusted: true

plt.style.use('ggplot')
fig,ax = plt.subplots(1,3,figsize=(12,10))
ax[0].plot(result['time'],result['h'],label='new')
ax[0].set(ylabel='height (m)',xlabel='time (days)',title='height')
ax[0].legend(loc='best')
ax[1].plot(result['time'],result['theta'],label='new')
out=ax[1].set(title=r'$\theta$ (K)')
out=ax[2].plot(result['time'],result['deltheta'],label='new')
out=ax[2].set(title=r'$\Delta \theta$ (K)')
```

```{code-cell} ipython3
:trusted: true


```
