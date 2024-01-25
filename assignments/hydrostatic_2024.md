---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(assign2_hydro)=
# Assign 2: Scale heights for typical atmospheric soundings

tentative deadline -- Friday 5pm

+++

## Tasks

1. Get a unique sounding for your assigned region and season
2. Plot the dewpoint and temperature soundings using metpy
3. Write a function to calculate the pressure scale height
4. Write a funcion to calculate the  density scale height
5. Plot the  vertical pressure profile vs. the hydrostatic pressure profile for your pressure scale height

+++

### 1. Getting a sounding

In the cell below, change the region, year, month and station to get a unique sounding for analysis (i.e. I'd like to spread out the soundings among regions and seasons).  The url for the Wyoming page is:  [https://weather.uwyo.edu/upperair/sounding.html](https://weather.uwyo.edu/upperair/sounding.html)

```{code-cell} ipython3
from a500.soundings.wyominglib import write_soundings
import numpy as np
sounding_dir = 'sounding_dir'
write = True
if write:
    region = 'samer'
    year = '2013'
    month= '7'
    start = '0100'
    stop = '0110'
    station = '71109'
    values=dict(region=region,year=year,month=month,start=start,stop=stop,station=station)
    write_soundings(values, sounding_dir)
```

```{code-cell} ipython3
from a500.soundings.wyominglib import read_soundings
wyoming_dict = read_soundings(sounding_dir)
sounding_dict = wyoming_dict['sounding_dict']
the_sounding = sounding_dict[(2013, 7, 1, 0)]
press = the_sounding['pres'].to_numpy() #hPa
dewpoint = the_sounding['dwpt'].to_numpy() #degC
temp = the_sounding['temp'].to_numpy() # degC
height = the_sounding['hght'].to_numpy() #m
tempK = temp + 273.15
pressPa = press*100.
height_km = height/1000.
```

```{code-cell} ipython3
the_sounding
```

###  2. Plot the sounding

```{code-cell} ipython3
from metpy.plots import SkewT
from metpy.units import units
from matplotlib import pyplot as plt
import numpy as np
fig,ax =plt.subplots(1,1,figsize=(8,8))
fig.clf()
skew_plot = SkewT(fig)
skew_plot.ax.set_title("metpy example")
skew_plot.ax.set(xlim=(0,25),ylim=(1000,600))
theta = np.array([0,10,20,30,40,50,60]) + 273.15
theta = theta*units("K")
skew_plot.plot_dry_adiabats(t0=theta)
skew_plot.plot_moist_adiabats()
skew_plot.plot_mixing_lines()
skew_plot.plot(press,temp,'r')
skew_plot.plot(press,dewpoint,'g');
```

### 3. Calculate the pressure scale height

+++

Here is equation 14 of the [hydrostatic balance notes](https://clouds.eos.ubc.ca/~phil/courses/atsc405/docs/hydro.pdf)

+++

$$\frac{ 1}{\overline{H_p}} =  \overline{ \left ( \frac{1 }{H} \right )} = \frac{\int_{0 }^{z}\!\frac{1}{H} dz^\prime  }{z-0} $$

where

$$H=R_d T/g$$

+++

a. Turn this into a python function called calc_scale_height that takes sounding vectors of temperature, pressure and height and returns
   the pressure scale height in meters

b.  Use this to find the pressure scale height in meters  as a scalar variable named Hbar

```{code-cell} ipython3
#
#  in this cell define a function called
#
#  calc_scale_height(T,p,z)
#  which takes vertical profiles of temperature, pressure and height and calculates the
#  pressure scale height in meters  -- save this into a variable named Hbar
#
```

### 4. Calculate the density scale height

Similarly, equation (23) of the [hydrostatic balance notes](https://clouds.eos.ubc.ca/~phil/courses/atsc500/docs/hydro.pdf)
is:

$$\frac{d\rho }{\rho} = - \left ( \frac{1 }{H} + 
                   \frac{1 }{T} \frac{dT }{dz} \right ) dz \equiv - \frac{dz }{H_\rho} $$
                   
Which leads to 

$$\frac{ 1}{\overline{H_\rho}}  = \frac{\int_{0 }^{z}\!\left [ \frac{1}{H} + \frac{1 }{T} \frac{dT }{dz} \right ] dz^\prime  }{z-0} $$

In the cell below write a python function called calc_dense_height

```{code-cell} ipython3
#
#  in this cell define a function called
#
#  calc_dense_height(T,p,z)
#  which takes vertical profiles of temperature, pressure and height and calculates the
#  density scale height in meters  -- save this into a variable named Hrho
#
```

### 5. How does the hydrostatic profile compare to the observed pressure sounding?

+++

Now check the hydrostatic approximation by plotting the pressure column against

$$p(z) = p_0 \exp \left (-z/\overline{H_p} \right )$$

vs. the actual sounding p(T):

```{code-cell} ipython3
#
#  In this cell make a plot with two lines, 
#
#  line 1: press (hPa) vs. height_km (vertical axis)
#  line 2: press p(z) from equation 5 (hPa) vs. height_km
#
#  include a legend that clear identifies the two lines
#  set the y axis limits from 0 to 10 km
#
```
