---
jupytext:
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(tropical_clouds)=
# Week 3 worksheet: Tropical clouds -- solution

+++

1. Download the [tropical_subset.nc](https://www.dropbox.com/scl/fi/dfj80s9q920ljni5aakfc/tropical_subset.nc?rlkey=2fc2wr2yb70e4i6l9c7gwcyj3&dl=0) netcdf file
   I put it in /Users/phil/Dropbox/phil_files/a405/data/tropical_subset.nc

+++

2. Find out what is in it with ncdump

```{code-cell} ipython3
!ncdump -h /Users/phil/Dropbox/phil_files/a405/data/tropical_subset.nc
```

The file contains a single timestep from the simulation I showd in [my day1 slides](https://phaustin.github.io/talks/cloud_talk.html).  The variables that we're interested in
right now are the absolute temperature TABS, the pressure $p$ and the pressure perturbation $PP$.

```{code-cell} ipython3
from pathlib import Path
import xarray as xr
the_file = Path.home() / "Dropbox/phil_files/a405/data/tropical_subset.nc"
the_ds = xr.open_dataset(the_file)
```

```{code-cell} ipython3
the_ds
```

```{code-cell} ipython3
the_ds['p'].data
```

## Taylor's series expansion of the equation of state

+++

Consider this equation from the
[Wikipedia entry on Taylor series](http://en.wikipedia.org/wiki/Taylor_series)

$$
\begin{align}
f(x,y) & \approx f(a,b) +(x-a)\, f_x(a,b) +(y-b)\, f_y(a,b)\nonumber \\
&  + \frac{1}{2!}\left[ (x-a)^2\,f_{xx}(a,b) + 2(x-a)(y-b)\,f_{xy}(a,b) +(y-b)^2\, f_{yy}(a,b) \right]
\end{align}
$$ (eq:taylor)
where $f_{xy} = \frac{ \partial^2 f}{\partial x \partial y }$, etc. You should be able to show
that if you expand $f=p=\rho R_d T$ about the point 
$p_0(z) = \rho_0(z) R_d T_0(z)$ where $p_0,\ \rho_0,\ T_0$ are the pressure,
density and temperature at height $z$ for a hydrostatic atmosphere.  Using {eq}`eq:taylor` with $a=\rho_0$ and $b=T_0$ you should be able to show that
to second order: 


$$
\frac{\Delta p}{p_0} = \frac{\Delta T}{T_0} + \frac{\Delta \rho}{\rho_0} + \frac{\Delta T \Delta \rho}{T_0 \rho_0}
$$ (eq:full)

Note that $\Delta p$, $\Delta T$, and $\Delta \rho$ are all functions of
(t,x,y,z).

If the atmosphere is close to hydrostatic balance, then we can expect the $\Delta$ differences to be small if $p_0$ is the hydrostatic pressure, and we can drop the
$\frac{ \Delta T \Delta \rho}{T_0 \rho_0}$ term and write

$$
\frac{\Delta p}{p_0} = \frac{\Delta T}{T_0} + \frac{\Delta \rho}{\rho_0}
$$

We will show later that away from active convection we also can expect $\frac{\Delta p }{p_0}$ to be small.



## Todo


1.  find the index of the vertical level that is closes to 500 m
2.   For that plot calculate histograms of all of the quantities in {eq}`eq:full`.  How much larger are the temperature and density terms that the pressure term?  How about the second order density x pressure term?

Userful reference:  [xarray plotting](https://docs.xarray.dev/en/latest/user-guide/plotting.html)

Hint for finding a level closest to 500 meters. Make sure you understand why this works:

```{code-cell} ipython3
import numpy as np
from matplotlib import pyplot as plt
heights = the_ds['z'].data
height_diff = heights - 500
the_lev = np.argmin(np.abs(height_diff))
print(f"{the_lev=} and {heights[the_lev]=}")
```

## Solution

```{code-cell} ipython3
Tvals = the_ds['TABS'][0,the_lev,:,:]
T0 = Tvals.mean(dim=['x','y'])
T_prime = Tvals - T0
T_term = T_prime/T0

pressPa = the_ds['p'][the_lev]*100.  # pascals
Rd = 287 #J/kg/K
rho_vals = pressPa/(Rd*Tvals)
rho0 = rho_vals.mean(dim=['x','y'])
rho_prime = rho_vals - rho0
rho_term = rho_prime/rho0

squared_term = rho_prime*T_prime/(rho0*T0)

press_perturb = the_ds['PP'][0,the_lev,:,:]
press_term = press_perturb/pressPa
```

```{code-cell} ipython3
fig, ax= plt.subplots(2,2,figsize = (10,10))
ax1, ax2, ax3, ax4 = ax.flat
T_term.plot.hist(ax = ax1)
rho_term.plot.hist(ax = ax2)
squared_term.plot.hist(ax=ax3)
press_term.plot.hist(ax=ax4)
ax1.set_title('T_term')
ax2.set_title('rho_term')
ax3.set_title('second order')
ax4.set_title('pressure perturb');
```

```{code-cell} ipython3

```
