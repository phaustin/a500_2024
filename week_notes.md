# Week notes

## Week 1

* Go over the [syllabus](index.md)

* Motivation -- [slides on boundary layer clouds and climate](https://phaustin.github.io/talks/cloud_talk.html)

### for Week 2

Read Chapter 1 of BLM.  For notation, especially virtual temperature, see the first 10 pages of Chapter 3 (thermodyanics) in Practical Meteorology

## Week 2

* Go over suppmental readings on Eulerian and Lagragian reference frames and frozen turbulence (Jardine lectures plus my Eulerian/Lagrangian notes)

* Introduce the dry les dataset and the week 3 notebook

### for week 3

* Read Stull chapter 3 and the Week 3 supplmentary notes
* Do the dry les notebook assignment -- soft deadline is Tuesday

## Week 3

* Thermodymamic review -- thermodynamic diagrams and scale height
* Buoyancy perturbations
* Solutions to the dry les notebook
* [Good tutorial on xarray](https://coecms-training.github.io/parallel/case-studies/loading_ensemble.html )
* How big are the pressure perturbation in the tropical_subset.nc notebook?

### For next week:

* Read [Dave Randalls scalling quickstudy](https://hogback.atmos.colostate.edu/group/dave/pdf/Dimensional_Analysis.pdf)
* Read Stull Chapter 4

## Week 4

### Tuesday 
  
  - notes on Taylor's series and Reynold's averaging
  - notes on the velocity scale
  - notes on virtual potential temperature
  
####  For next Tuesday

  - Do Stull Chapter 4 problems 1, 3, 5
  - For the tropical subset dataset plot soundings of the potetial temperature flux, the temperature flux and the virtual potential temperature flux -- are they different
  - For the same notebook, plot the turbulent kinetic energy scaled by the convective velocity scale and the surface velocity scale -- are they different?
  
###  Thursday

   - Focus on Stull sections 4.4.2 and 4.4.3 on moisture and heat fluxes
   - Look at sensible and latent fluxes in this notebook: {ref}`tropical_fluxes`
   - Go over my notes on [moist static energy](https://www.dropbox.com/scl/fi/sosiyoxa9bzhecea5qas9/hydro.pdf?rlkey=7wll6s0yc4t0dlojzx56082iw&dl=0) 
   - Prep for the Clausius-Clayron equation: [notes on Maxwell's relations](https://www.dropbox.com/scl/fi/o7d278acumkgmwe4y6qlu/clausius.pdf?rlkey=ktd5fvdwaz7ishuxozwmf6kwa&dl=0)
   - New example articles covering material from Chapter 7:  [Betts Horton Lecture](https://journals.ametsoc.org/view/journals/bams/85/11/bams-85-11-1673.xml) and [Betts Land Surface Coupling review](https://agupubs.onlinelibrary.wiley.com/doi/10.3894/James.2009.1.4)

   #### For next Tuesday:
   
   - Read Stull Chapter 5
   - Read my [static energy notes](https://www.dropbox.com/scl/fi/zuk9evzf47qdsxi9tvgx7/thermo.pdf?rlkey=hbz3bpt6gxv5ly8rg1njfj9e4&dl=0)
   - Read my derivation of the [Clausius-Clapyron equation](https://www.dropbox.com/scl/fi/o7d278acumkgmwe4y6qlu/clausius.pdf?rlkey=ktd5fvdwaz7ishuxozwmf6kwa&dl=0)
     

## Week 5

### Tuesday

- Thermodyamics -- important points

    - Equations 39 and 41 for the moist and liquid static energies: 

      $$
      \begin{align}
      s_v &= c_p T + l_v r_v + gz \\
      s_l & = c_p T - l_v r_l + gz 
      \end{align}
      $$
    
    - Equation 54 and 55  for the equivalent potential temperature and liquid water potential temperature
    
       $$
        \begin{align}
         \theta_e &= \theta \exp \left ( \frac{l_v r_{sat}}{c_p T} \right )\\
         \theta_l &= \theta \exp \left ( - \frac{l_v r_l}{c_p T} \right )
        \end{align}
       $$
  
    - Note that $s_v$, $s_l$, $\theta_v$ and $\theta_l$ all approximately label the same moist adiabat on a tephigram, because they are all approximately conserved for adiabatic ascent and descent

- Thermodynamics: {ref}`rootfind`

- Thermodynamics: {ref}`moist_adiabats`

- Chapter 4/5 topics

  - Chapter 4: [pressure perturbation notes](https://www.dropbox.com/scl/fi/7tkg65ar1u9emumxervu5/pressure_perturb.pdf?rlkey=gu3miynu1k28cs1985mrxxu4h&dl=0)
  - Chapter 5: Bussinger article on the [critcial Richardson number](https://www.dropbox.com/scl/fi/yqegu0q64a2t6sipms7t4/bussinger_critical_ri.pdf?rlkey=34m6gyzz5lv9oaxum8xx7ynge&dl=0)
  
### Thursday


- [Assignment 3](https://phaustin.github.io/a500_2024/week_notes.html#for-next-tuesday) due:  Monday

- Project decision tree

  - Dry or cloudy boundary layer?
  - Stable or unstable?
  - GCMs, LES, or observations?
  
- Topic ideas

  - Compare GCM boundary layer performance using the CMIP6 dataset for different models
    - surface fluxes, shear, boundary layer height for similar large scale forcings
  - Compare LES results or tower measureements against a parameterization
  - Verify scaling relationships using LES
  - Fourier/wavelet analysis of LES boundary layer data  (Stull Figure 5.16)
  - Conditional sampling of LES or aircraft data
  - New article: [Canadian Climate Model boundary layer parameterization](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2018MS001532)
  
- Chapter 5 topics

  - Surface layer scaling:
    - [Velocity scale notes part 2](https://www.dropbox.com/scl/fi/ezjs46bsqegvnzasujnic/velocity_scales.pdf?rlkey=tkgf0zu4kxjnpmssa3zwglp2i&dl=0)
    - [Surface layer scaling notes](https://www.dropbox.com/scl/fi/e6cq3sodf0fq2rwuynsfm/boussinesq.pdf?rlkey=8josihsmcn1fskhl6mvnlu4eh&dl=0)
    - [Boussinesq approximation notes](https://www.dropbox.com/scl/fi/e6cq3sodf0fq2rwuynsfm/boussinesq.pdf?rlkey=8josihsmcn1fskhl6mvnlu4eh&dl=0)
    
- For next Tuesday

  - For next Tuesday read Chapter 6 through section 6.5 and do problems 6.14, 6.15, 6.16, 6.17

## Week 6

### Tuesday

- Finish Chapter 6 on TKE and closure

- Notes on [Mellor Yamada TKE parameterization](https://www.dropbox.com/scl/fi/hdbpj7stnutwva85njr2k/mellor_yamada_notes.pdf?rlkey=kxlb7tpfo3bc2ogyzt1iht936&dl=0) (just page 1-2 for now)

- Revisit the dry les notebook -- question for post-break: why is the inversion height growing as $\sqrt{\text{time}}$?  see: {ref}`dry_lesII`

- Introduce Cabauw tower data:  [Cabauw home page](https://www.knmi.nl/research/observations-data-technology/projects/cabauw-in-situ-measurements), [wikipedia entry](https://en.wikipedia.org/wiki/KNMI-mast_Cabauw)
- [LES simulations focussed on Cabauw](https://www.dropbox.com/scl/fi/oewkjlpdod168tvg3lok3/cabauw_les.pdf?rlkey=kigrdkur74r6irafyhcn7pr40&dl=0)
- Data for July and December, 2014: [cabauw.zip](https://www.dropbox.com/scl/fi/he3cyb6y2nd36gm959rke/cabauw.zip?rlkey=calxnyzv4yct8bo09e4p2o06u&dl=0)
- Notebook to read the data: {ref}`read_cabauw`


#### For Thursday, read the first 10 pages of Chapter 7

### Thursday

* Surface layer review and first order closure

* Go over how to do first order closure for $\theta$ using {ref}`simple_integrator`

* For break -- finish Chapter 7  -- work on proposals/papers


## Week 7

### Tuesday

- Go over the material from Stull Chapter 7 page 267-271 on the Businger-Dyer relationships, which is repeated in Chapter 9 p. 383-385.

- Finish my [Surface layer scaling notes](https://www.dropbox.com/scl/fi/0bip672b25he2ikr2honz/surface_layer.pdf?rlkey=iurhmsxfrbxkodzkzqxoa66yd&dl=0) to get the drag coefficients 
  and  $C_D$ and $C_H$

- Paper: Surface-layer scaling at Cabauw: [Verkaik and Holtslag](https://login.ezproxy.library.ubc.ca/login?qurl=https://link.springer.com%2farticle%2f10.1007%2fs10546-006-9121-1)

  - Take home point from that paper: Surface layer scaling can be disturbed by upstream changes in  
    surface roughness (although it still does pretty well)

  - Figure 5 on page 710 shows the agreement/disagreement with Businger-Dyer relationships
    depending on upstream conditions/wind direction

- Side note – an interesting [historical note from Businger](https://www.dropbox.com/scl/fi/961z9gwv9h9gh1a7ka0ty/businger_history_87.pdf?rlkey=5zbjdff8vn3349e9y3xrqx0uh&dl=0) on how Businger and Dyer independently
  came up with the surface layer relationships for $\Phi_m$ and $\Phi_h$

- For a detailed derivation of $\Phi_{\mathrm{m}}=(1-\alpha \mathrm{Ri})^{-1 / 4} \mathrm{~s}$
  see [Fleagle and Businger, 1980, p. 275-277](https://www.dropbox.com/scl/fi/o43cv43ymuxj35nti2c2b/fleagle_bussinger_1980.pdf?rlkey=eb98rznjih3efu185wxeljsd5&dl=0)
  
### Thursday

- Here’s a Jupyter notebook that implements {ref}`businger-dyer`
- Assignment 5: Modify the {ref}`simple_integrator` notebook
  so that it works with a specified surface temperature instead of a fixed surface flux. Use the Businger-Dyer drag coefficients to calculate the flux. To keep the layer growing you can specify that the surface temperature is a couple of degrees warmer than the air just above it (make that tmeperature difference an adjustable parameter). Try to adjust your parameters so you produce about 50-100  of buoyancy flux.

## Week 8

- Go over the KNMI data download api for Cabauw, and CMiP6 notebooks for precipitation
  and the Betts surface energy budget analysis [Betts 2009 fig 10](https://agupubs.onlinelibrary.wiley.com/doi/10.3894/James.2009.1.4)
  
- {ref}`cesar_tower`
- {ref}`cesar_surface`
- {ref}`cmip6_historical`
- {ref}`betts_data_fetch`
- {ref}`betts_diurnal_lcl`

### For Tuesday

- Read Stull Chapter 11 thorugh page 458 (mixed layers)
- Also  Read [Garratt Chapter 6](https://www.dropbox.com/scl/fi/vqvpsg4isduv02cth3g98/garratt_ch6.pdf?rlkey=rqp14mmbk6pcm3o1fhmfmvsbt&dl=0)
- Finish the surface layer assignment

## Week 9

### Tuesday

#### Dry mixed layers 1

- Stull p. 271 Section 7.4.3

- Stull Chapter 11 p. 453-458

- Garratt pp. 151-159

- [Liebniz review notes](https://www.dropbox.com/scl/fi/s75gp821y8riznrjioem4/liebniz.pdf?rlkey=u13g1jtrnqx55t4f90uf3gzuo&dl=0)

- [mixed layer notes](https://www.dropbox.com/scl/fi/8l9qb7mqtfhs58b4s7jf6/mixed_layer.pdf?rlkey=a2av8cmvjvvti44723hn69acw&dl=0)
  
### Thursday

#### Dry mixed layers 2

- Coverage: Entrainment zone: Stull pp. 473-483

- How do we get entrainment into the mixed layer model?

  - Recall the difference between {ref}`dry_lesII` and  {ref}`simple_integrator`
  - My [mixed layer jump notes](https://www.dropbox.com/scl/fi/b53feva305h7yqnkq35db/mixed_layer_jump.pdf?rlkey=8tavsjdviy1js1zol69772fcc&dl=0)
  - Put this into a notebook: {ref}`dry_mixed_layer`
    - [download dry_mixed_layer.ipynb](https://www.dropbox.com/scl/fi/e2mcdo9zfxclizf334efl/dry_mixed_layer.ipynb?rlkey=r9q8veh2ul9ck6rm73013pjwm&dl=0)
  

### For Tuesday

- Read [Stephan de Roode's stratocumulus notes](https://www.dropbox.com/scl/fi/6ep2orutcgusmsyyfpytg/deroode_strat.pdf?rlkey=64yhkwd5mu9a3g2ioaw89bran&dl=0).  This is an excerpt from his [
T. U. Delft cloud course](https://www.dropbox.com/scl/fi/n6scqt3wql8otdfvsif1r/de_roode_clouds.pdf?rlkey=v82zcoh7doaib9xvy1mjh8zj1&dl=0)
- Read [Nuijens and Siebesma stratocumulus review](https://www.dropbox.com/scl/fi/045ir1w65lwh0rm4hot4z/nuijens_siebesma_review.pdf?rlkey=vdtgfpwatcuq794ijk4gl29ak&dl=0)

- A useful resource: the [ECMWF parameterization lecture notes](https://confluence.ecmwf.int/display/OPTR/Parametrization)
 - [dropbox folder](https://www.dropbox.com/scl/fo/cc7e1fczy5zhe3h3m5ow1/h?rlkey=fgaopp026vu99mqm4nfz2fqic&dl=0)
 
## Week 10

### Tuesday

- [de Roode lecture slides Part I](https://www.dropbox.com/scl/fi/85ebprdn52ar4c6c1e8le/Roode_1_BB.pdf?rlkey=3lyhxjt7hwyszsedq3mmb4owt&dl=0)
- [de Roode lecture slides Part II](https://www.dropbox.com/scl/fi/hq7bnhb5dnvzmsehnhxgd/Roode_2_BB.pdf?rlkey=go05jddf8dm0qjb1ztytazl40&dl=0)
- [Gesso et al. 2014 equilibrium boundary layer](https://www.dropbox.com/scl/fi/pdodmk9405d5dc4f4obv6/deroode_Dal_Gesso_etal_2014.pdf?rlkey=ycmxd3g56q9mh5sus0qxqi8kj&dl=0)
- [Stevens entrainment review 2002](https://www.dropbox.com/scl/fi/41n9v7pj3x0n2tu27ca4o/Stevens-2002-Quarterly_Journal_of_the_Royal_Meteorological_Society.pdf?rlkey=u5705q214gzpe3r94doozyrqy&dl=0)

### Thursday 

- Continue with [de Roode lecture slides Part II](https://www.dropbox.com/scl/fi/hq7bnhb5dnvzmsehnhxgd/Roode_2_BB.pdf?rlkey=go05jddf8dm0qjb1ztytazl40&dl=0)

- Does it matter whether you predict or diagnose the inversion jump? {ref}`mixed_layer_jump`

### For Tuesday

- Read [Gesso et al. 2014 equilibrium boundary layer](https://www.dropbox.com/scl/fi/pdodmk9405d5dc4f4obv6/deroode_Dal_Gesso_etal_2014.pdf?rlkey=ycmxd3g56q9mh5sus0qxqi8kj&dl=0)  -- along with the [
T. U. Delft cloud course](https://www.dropbox.com/scl/fi/n6scqt3wql8otdfvsif1r/de_roode_clouds.pdf?rlkey=v82zcoh7doaib9xvy1mjh8zj1&dl=0) chapter 5

- Coming up: More on Chapter 7/heat waves, starting with [Vargas Zepetello et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2019GL082220)

## Week 11

### Tuesday

- Useful background material for reading [Vargas Zepetello et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2019GL082220)

  - [E340 feedback notes](https://www.dropbox.com/scl/fi/y3m3abh6ktiac8w5q3fvs/e340_feedback_notes.pdf?rlkey=e1hnv7moee9xg7ob6bf3r0npi&dl=0)

  - [A more advanced feedback introduction](https://www.dropbox.com/scl/fi/ht8pkmiq3bx0zu7g86w3g/gerard_roe_feedbacks_2009.pdf?rlkey=pxk5jql3th5pcxazoicbigli0&dl=0)

  - [How to compute $\Delta R$/$\Delta x$](https://climatemodels.uchicago.edu/modtran/)

  - [Vargas Zeppetello et al., 2022 -- the physics of heat waves](https://journals.ametsoc.org/view/journals/clim/35/7/JCLI-D-21-0236.1.xml)

  - [Vargas Zeppetello et al, 2020a, Variance of summertime temperatures over land]( https://journals.ametsoc.org/view/journals/clim/33/13/jcli-d-19-0887.1.xml)

  - [Vargas Zeppetello et al., 2020b, Sources of variance of summertime temperatures](https://journals.ametsoc.org/view/journals/clim/33/9/jcli-d-19-0276.1.xml)


