---
jupytext:
  formats: ipynb,md:myst
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

(moist_adiabats)=
# Moist adiabats and the LCL

This notebook shows how to find the lifting condensation level of a sounding, and identify $\theta_{es}$ for the moist adiabat going through cloud base.

```{code-cell} ipython3
import numpy as np
import pandas as pd
from pprint import pformat

from a500.thermo.constants import constants as c
from a500.thermo.thermlib import convertSkewToTemp, convertTempToSkew
from a500.skewT.fullskew import makeSkewWet,find_corners,make_default_labels
```

```{code-cell} ipython3
from a500.soundings.wyominglib import write_soundings, read_soundings
from matplotlib import pyplot as plt
```

## Grab a Little Rock sounding

Set get_data = True to fetch the Wyoming sounding data from the website and store it.

```{code-cell} ipython3
get_data = True
values=dict(region='naconf',year='2012',month='7',start='0100',stop='3000',station='72340')
if get_data:
    write_soundings(values, 'littlerock')
soundings= read_soundings('littlerock')
```

```{code-cell} ipython3
soundings['sounding_dict'].keys()
```

## Select one sounding -- July 17, 2012 at 0 UCT

```{code-cell} ipython3
the_time=(2012,7,17,0)
sounding=soundings['sounding_dict'][the_time]
sounding.columns
```

## Save the metadata for plotting

```{code-cell} ipython3
title_string=soundings['attributes']['header']
index=title_string.find(' Observations at')
location=title_string[:index]
print(f'location: {location}')

units=soundings['attributes']['units'].split(';')
units_dict={}
for count,var in enumerate(sounding.columns[1:]):
    units_dict[var]=units[count]
#
# use the pretty printer to print the dictionary
#
print(f'units: {pformat(units_dict)}')
```

## Convert temperature and dewpoint to skew coords

```{code-cell} ipython3
skew=35.
triplets=zip(sounding['temp'],sounding['dwpt'],sounding['pres'])
xcoord_T=[]
xcoord_Td=[]
for a_temp,a_dew,a_pres in triplets:
    xcoord_T.append(convertTempToSkew(a_temp,a_pres,skew))
    xcoord_Td.append(convertTempToSkew(a_dew,a_pres,skew))
```

## Plot the sounding, making the sounding lines thicker

```{code-cell} ipython3
def label_fun():
    """
    override the default rs labels with a tighter mesh
    """
    from numpy import arange
    #
    # get the default labels
    #
    tempLabels,rsLabels, thetaLabels, thetaeLabels = make_default_labels()
    #
    # change the temperature and rs grids to get a finer mesh
    #
    tempLabels = range(-40, 50, 2)
    rsLabels = [0.1, 0.25, 0.5, 1, 2, 3] + list(np.arange(4, 28, 2)) 
    return tempLabels,rsLabels, thetaLabels, thetaeLabels
```

```{code-cell} ipython3
fig,ax =plt.subplots(1,1,figsize=(8,8))
corners = [10, 35]
ax, skew = makeSkewWet(ax, corners=corners, skew=skew,label_fun=label_fun)
#ax,skew = makeSkewWet(ax,corners=corners,skew=skew)
out=ax.set(title=title_string)
xcorners=find_corners(corners,skew=skew)
ax.set(xlim=xcorners,ylim=[1000,400]);
l1,=ax.plot(xcoord_T,sounding['pres'],color='k',label='temp')
l2,=ax.plot(xcoord_Td,sounding['pres'],color='g',label='dew')
[line.set(linewidth=3) for line in [l1,l2]];
```

## Find the $\theta_{es}$ of the  LCL

The thermo.thermlib docs are [here](https://phaustin.github.io/a405_lib/full_listing.html#module-a405.thermo.thermlib)

```{code-cell} ipython3
from a500.thermo.thermlib import (find_Tmoist,find_thetaep,find_rsat,
                                 find_Tv,find_lcl,find_thetaes,find_thetaet)
#
# find thetae of the surface air, which is at index 0
#
sfc_press,sfc_temp,sfc_td =[sounding[key][0] for key in ['pres','temp','dwpt']]
#
# convert to Kelvin
#
sfc_press,sfc_temp,sfc_td = sfc_press*100.,sfc_temp+c.Tc,sfc_td+c.Tc
```

### What is the LCL of this air?

```{code-cell} ipython3
Tlcl, plcl=find_lcl(sfc_td, sfc_temp,sfc_press)
```

```{code-cell} ipython3
print(f'found Tlcl={Tlcl:0.1f} K, plcl={plcl:0.1f} Pa')
```

```{code-cell} ipython3
#  convert to mks and find surface rv and thetae
#
sfc_rvap = find_rsat(sfc_td,sfc_press)
lcl_rvap = find_rsat(Tlcl,plcl)
sfc_thetae=find_thetaes(Tlcl,plcl)
press=sounding['pres'].values*100.
#
# find the index for 70 hPa pressure -- searchsorted requires
# the pressure array to be increasing, so flip it for the search,
# then flip the index.  Above 70 hPa thetae goes bananas, so
# so trim so we only have good values
#
toplim=len(press) - np.searchsorted(press[::-1],.7e4)
clipped_press=press[:toplim]
#
# find temps, rv and rl along that adiabat
#
adia_temps= np.array([find_Tmoist(sfc_thetae,the_press) 
                      for the_press in clipped_press])
adia_rvaps = find_rsat(adia_temps,clipped_press)
adia_rls = sfc_rvap - adia_rvaps
env_temps = (sounding['temp'].values + c.Tc)[:toplim]
env_Td = (sounding['dwpt'].values + c.Tc)[:toplim]
height = sounding['hght'].values[:toplim]
pairs = zip(env_Td,clipped_press)
env_rvaps= np.array([find_rsat(td,the_press) for td,the_press in pairs])
env_Tv = find_Tv(env_temps,env_rvaps)
adia_Tv = find_Tv(adia_temps,adia_rvaps,adia_rls)
xcoord_thetae=[]
press_hPa = clipped_press*1.e-2
#
# convert the adiabatic thetae sounding to skewT coords
#
for a_temp,a_press in zip(adia_temps - c.Tc,press_hPa):
    out=convertTempToSkew(a_temp,a_press,skew)
    xcoord_thetae.append(out)
ax.plot(xcoord_thetae,press_hPa,color='r',label='thetae',linewidth=3.)
xlcl=convertTempToSkew(Tlcl - c.Tc,plcl*0.01,skew)
ax.plot(xlcl,plcl*0.01,'bo',markersize=8)
display(fig)
```
