---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

(cloud_capped_index)=
# Cloud capped boundary layer

This is the table of contents for a series of notebooks that show how to build a mixed layer model that includes moist thermodynamics and entrainment


## References


- [Stull BLM Chapter 13](https://www.dropbox.com/scl/fi/yaxd27icivz7a7qu7tifn/stull_blm_springer.pdf?rlkey=v0hqkqvd9v8rpcqfxmq62tt10&dl=0)
- [de Roode chapter 5](https://www.dropbox.com/scl/fi/n6scqt3wql8otdfvsif1r/de_roode_clouds.pdf?rlkey=v82zcoh7doaib9xvy1mjh8zj1&dl=0)
- [Stevens entrainment review](https://www.dropbox.com/scl/fi/41n9v7pj3x0n2tu27ca4o/Stevens-2002-Quarterly_Journal_of_the_Royal_Meteorological_Society.pdf?rlkey=u5705q214gzpe3r94doozyrqy&dl=0)


## Notebooks

- {ref}`mixed_layer_jump` demonstrates that diagnosing and predicting the jump $\Delta \theta$ at the top of the mixed layer is equivalent in dry boundary layers
- {ref}`add_subsidence` shows how a boundary layer equilibrates when subsidence is included
- {ref}`vapor_flux` adds water as a conserved variable, plus radiative cooling at the top of the boundary layer
- {ref}`radcool` makes the entrainment rate depend on the radiative cooling
- {ref}`nicholls_turton` calculates the NT entrainment rate from the de Roode slides
- {ref}`closure` compares 3 boundary layer closures

```python

```
