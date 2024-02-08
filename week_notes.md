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
<<<<<<< Updated upstream
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
  
    - Note that $s_v$, $s_l$, $\theta_v$ and $theta_l$ all approximately label the same moist adiabat on a tephigram, because they are all approximately conserved for adiabatic ascent and descent

- Thermodynamics: {ref}`rootfind`

- Thermodynamics: {ref}`moist_adiabats`

- Chapter 4/5 topics

  - Chapter 4: [pressure perturbation notes](https://www.dropbox.com/scl/fi/7tkg65ar1u9emumxervu5/pressure_perturb.pdf?rlkey=gu3miynu1k28cs1985mrxxu4h&dl=0)
  - Chapter 5: Bussinger article on the [critcial Richardson number](https://www.dropbox.com/scl/fi/yqegu0q64a2t6sipms7t4/bussinger_critical_ri.pdf?rlkey=34m6gyzz5lv9oaxum8xx7ynge&dl=0)
  
=======
     - Read my [static energy notes](https://www.dropbox.com/scl/fi/tfgz28syrhn1zk6y066nm/thermo.pdf?rlkey=eigclji5ypji0p12cfww6w2x1&dl=0) through page 6
     - Read my derivation of the [Clausius-Clapyron equation](https://www.dropbox.com/scl/fi/o7d278acumkgmwe4y6qlu/clausius.pdf?rlkey=ktd5fvdwaz7ishuxozwmf6kwa&dl=0)
     
* Week 5 - Tuesday

  - Hand in Stull Chapter 4 problems 1, 3, 5, plus notebook with virtual temperature flux and turbulent kinetic energy profiles

  - Working with moisture variables, the most important are 
>>>>>>> Stashed changes
