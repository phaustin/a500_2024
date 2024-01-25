---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Working with LES data: dry boundary layer

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

the_file = Path.home() / "Dropbox/phil_files/a500/data" / "case_60_10.nc"
if not the_file.exists():
    raise ValueError(f"{the_file} not found")
```

## Find the netcdf file an dump its contents

```{code-cell} ipython3
the_file
```

```{code-cell} ipython3
!ncdump -h /Users/phil/Dropbox/phil_files/a500/data/case_60_10.nc
```

Netcdf file layout:  10 groups corresponding to 10 different ensemble members.  Small slice of larger domain of LES run with surface heat flux of 60 W/m^2 and stable layer with dT/dz = 10 K/km.  Snapshots every 10 minutes for 8 hours.

+++

## Open the first ensemble member c1

Look at the last 5 values of z, pressure

From the ncdump we know that there are global variables and attributes as
well as the 10 ensemble members.  So get two xarray dataset pointers:

- ds1 for the first ensemble member
- the_ds for the global variables

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
ds1 = xr.open_dataset(the_file,group="c1")
the_ds = xr.open_dataset(the_file)
```

```{code-cell} ipython3
the_ds['z'][-5:]
```

```{code-cell} ipython3
ds1
```

### Get variable vectors and dimension sizes

```{code-cell} ipython3
temp = ds1['TABS']
wvel= ds1['W']
times = the_ds['time']
z=the_ds['z']
y = the_ds['y']
x = the_ds['x']
press=the_ds['press']
ntimes,nz,ny,nx = ds1.sizes.values()
print(f"{(ntimes,nz,ny,nx)=}")
```

```{code-cell} ipython3
y
```

## check height and pressure

```{code-cell} ipython3
(z[-5:].data,press[-5:].data)
```

## Function to convert to $\theta$

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
def make_theta(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.
    cpd=1004.
    theta=temp*(p0/press)**(Rd/cpd)
    
    return theta
    
```

## Get the horizontal average

```{code-cell} ipython3
temp_mean=temp.mean(dim=["x","y"])
```

```{code-cell} ipython3
temp_mean[0,-5:]
```

```{code-cell} ipython3
## Plot the timestep theta,height profiles for c1
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: false
---
fig,ax=plt.subplots(1,1,figsize=(8,8))
ntimes, nheights = temp_mean.shape
for i in np.arange(0,ntimes,3):
    theta = make_theta(temp_mean[i,:],press)
    ax.plot(theta,z)
ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',
       title='LES dry run:  surface flux=60 $W\,m^{-2}$, $\Gamma$=10 K/km');

    
```

## Assignment -- targeting Tuesday

+++

- Write functions that find the ensemble mean $\langle \zeta \rangle$ and the perturbation about that mean $\zeta^\prime$ an arbitrary variable $\zeta$
- Use those functions to calculate the horizontally averaged vertical entropy flux $\overline{w^\prime\,\theta^\prime}$ as a function of height and make a plot similar to the figure above

+++

## Assignment solution

+++

### Collect all 10 ensemble members into a dicionary

```{code-cell} ipython3
ensemble_names = [f"c{i}" for i in np.arange(1,11)]
```

```{code-cell} ipython3
ensemble_names
```

```{code-cell} ipython3
ds_dict = {}
for count, name in enumerate(ensemble_names):
    ds = xr.open_dataset(the_file,group=name)
    ds_dict[count] = ds
```

```{raw-cell}
### Function to turn dictionary into DataArray 
```

```{code-cell} ipython3
import numpy.typing as npt
def make_array(var_dict: dict, 
               varname: str,
               times: npt.ArrayLike,
               x: npt.ArrayLike, 
               y: npt.ArrayLike,
               z: npt.ArrayLike, 
               press:npt.ArrayLike):
    # given a dictionary of ensemble members, 
    # create a new data array containing variable varname
    #
    n_ensembles = len(var_dict)
    #
    # get shapes and attrs from first ensemble member
    #
    attrs = var_dict[0][varname].attrs
    print(f"{attrs=}")
    ntimes, nz, ny, nx = var_dict[0][varname].shape
    var_array = np.empty((n_ensembles,ntimes,nz,ny,nx))
    for ensemble in range(n_ensembles):
        print(f"working on {ensemble=}")
        var_array[ensemble,...] = var_dict[ensemble][varname][...]
    ensemble_coord = list(range(n_ensembles))
    coords = {'ensemble' : ensemble_coord,'time':times, 'z': z, 'y' : y, 'x' : x}
    dims = ('ensemble','time','z','y','x')
    the_array = xr.DataArray(var_array,coords=coords,dims=dims,attrs=attrs,name=varname)
    return the_array
```

### Function to turn TABS and press membeers from a  dictionary into a 5-d theta array

#### First try this without broadcasting

Since pressure is a 1-d vec of length 130 you can't multiply that shape
with a 5 dimensional ensemble and have the make_theta function work.
So loop over all dimensions except z so that shapes will match

This takes a considerable amount of time in python

```{code-cell} ipython3
def make_theta_array(var_dict: dict, 
               times: npt.ArrayLike,
               x: npt.ArrayLike, 
               y: npt.ArrayLike,
               z: npt.ArrayLike, 
               press:npt.ArrayLike):
    #
    # given a dictionary of ensemble members, 
    # create a new data array converting TABS and press to 
    # potential temperature
    #
    n_ensembles = len(var_dict)
    #
    # get shapes and attrs from TABS for first ensemble member
    #
    ntimes, nz, ny, nx = var_dict[0]['TABS'].shape
    attrs = var_dict[0]['TABS'].attrs
    print(f"{attrs=}")
    theta_array = np.empty((n_ensembles,ntimes,nz,ny,nx))
    for ensemble in range(n_ensembles):
        print(f"working on {ensemble=}")
        for timestep in range(ntimes):
            the_tabs = var_dict[ensemble]['TABS'][timestep,...]
            for xindex in range(len(x)):
                for yindex in range(len(y)):
                   theta_array[ensemble,timestep,:,yindex,xindex]= \
                        make_theta(the_tabs[:,yindex,xindex],press)
    ensemble_coord = list(range(n_ensembles))
    coords = {'ensemble' : ensemble_coord,'time':times, 'z': z, 'y' : y, 'x' : x}
    dims = ('ensemble','time','z','y','x')
    the_array = xr.DataArray(theta_array,coords=coords,dims=dims,attrs=attrs,name='theta')
    return the_array
```

####  Now do this with broadcasting

We need to promote press into a 5-d array that will broadcast with
the ensemble array which has shape [10, 48,130, 20, 25]  That means
that press needs to have shape [1,1,130,1,1].  We can do htat with
[np.expand_dims](https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html)  The rules
for broadcasting are covered here:  [numpy.broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)

```{code-cell} ipython3
def make_theta_broadcast(var_dict: dict, 
               times: npt.ArrayLike,
               x: npt.ArrayLike, 
               y: npt.ArrayLike,
               z: npt.ArrayLike, 
               press:npt.ArrayLike):
    #
    # given a dictionary of ensemble members, 
    # create a new data array converting TABS and press to 
    # potential temperature
    #
    n_ensembles = len(var_dict)
    #
    # get shapes and attrs from TABS for first ensemble member
    #
    ntimes, nz, ny, nx = var_dict[0]['TABS'].shape
    attrs = var_dict[0]['TABS'].attrs
    print(f"{attrs=}")
    #
    # for broadcasting give press the shape [1,1,130,1,1]
    #
    press_array = np.expand_dims(press,axis=(0,1,-1,-2))
    tabs_array = np.empty((n_ensembles,ntimes,nz,ny,nx))
    for ensemble in range(n_ensembles):
        print(f"working on {ensemble=}")
        tabs_array[ensemble,...] = var_dict[ensemble]['TABS'][...]
    theta_array = make_theta(tabs_array,press_array)
    ensemble_coord = list(range(n_ensembles))
    coords = {'ensemble' : ensemble_coord,'time':times, 'z': z, 'y' : y, 'x' : x}
    dims = ('ensemble','time','z','y','x')
    the_array = xr.DataArray(theta_array,coords=coords,dims=dims,attrs=attrs,name='theta')
    return the_array
```

Here's how you use expand_dims to add axis on either size of the z axis

```{code-cell} ipython3
out=np.expand_dims(press,axis=(0,1,-1,-2))
out.shape
```

### create a theta dataset and write to disk

We'll write theta to disk as zarr file.  zarr is a successor to netcdf optimized for use in the cloud.  See [https://zarr.dev/](https://zarr.dev/)

```{code-cell} ipython3
import zarr
zarrfile = 'theta.zarr'
write = True
if write:
    theta  = make_theta_broadcast(ds_dict,times,x,y,z,press)
    theta.to_zarr(zarrfile,mode='w')
else:
    theta_ds = xr.open_zarr(zarrfile)
    theta = theta_ds['theta']
```

```{code-cell} ipython3
theta
```

### create a wvel array

```{code-cell} ipython3
wvel = make_array(ds_dict,'W',times,x,y,z,press)
```

```{code-cell} ipython3
### Do the ensemble and horizontal flux average
```

```{code-cell} ipython3
w_mean = wvel.mean(dim=['ensemble'])
w_perturb = wvel - w_mean
theta_mean = theta.mean(dim=['ensemble'])
theta_perturb = theta - theta_mean
theta_flux = theta_perturb*w_perturb
ensemble_mean = theta_flux.mean(dim=['ensemble'])
ensemble_horizavg = ensemble_mean.mean(dim=['x','y'])
ensemble_horizavg.shape
```

```{code-cell} ipython3
the_ds.attrs
```

```{code-cell} ipython3
fig, ax = plt.subplots(1,1,figsize=(10,10))
for timestep in np.arange(0,ntimes,3):
    ax.plot(ensemble_horizavg[timestep,:],z,label=timestep)
ax.legend(loc='best')
heat_flux = the_ds.attrs['heat_flux_W_m2']
gamma = the_ds.attrs['gamma_K_km']
ax.grid(True)
ax.set_title(f"theta flux with heat flux = {heat_flux} W/m2 and inversion strength = {gamma} K/km");
```

```{code-cell} ipython3

```
