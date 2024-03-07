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

# Cabauw surface data

```{code-cell} ipython3
import requests
from pathlib import Path
import json

json_file = Path.home()/ '.knmi_key.json'
write=False
if write:
    #
    # uncomment the line below and add your key the first time to create .knmi_key.json
    # don't check code with your api key into github, instead
    # read it from the json file
    #
    # knmi_key=xxxxxxxxx
    #
    with open(json_file,'w') as outfile:
        json.dump(knmi_dict,outfile)

with open(json_file,'r') as infile:
    api_dict = json.load(infile)
api_key = api_dict['knmi_api']

headers = {
    'accept': 'application/json',
    'Authorization': api_key
}


params = {
    'maxKeys': '10',
    'sorting': 'desc',
    'orderBy': 'filename',
}

response = requests.get(
    'https://api.dataplatform.knmi.nl/open-data/v1/datasets/cesar_surface_flux_lb1_t10/versions/v1.0/files',
    params=params,
    headers=headers,
)
out = response.json()
for the_file in out["files"]:
    print(the_file.get("filename"))
```

```{code-cell} ipython3

```
