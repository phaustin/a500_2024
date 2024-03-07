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

# Cabauw tower data

The KNMI data server uses [REST](https://www.redhat.com/en/topics/api/what-is-a-rest-api) (representational state transfer) to return datasets from requests sent via http to the server.  In python, this is done using the 

Resources:

- [KNMI api examples](https://developer.dataplatform.knmi.nl/open-data-api)
- [openapi test page](https://tyk-cdn.dataplatform.knmi.nl/open-data/index.html)
- [curl to python converter](https://curlconverter.com)
- [Fifty years of atmospheric boundary layer research at Cabauw](https://link.springer.com/article/10.1007/s10546-020-00541-w)

+++

## Get a filelist

- timestamp doesn't seem to matter, just get as many filenames as you need
by incresing the 'maxKeys' parameter below
- requires an api key from [here](https://developer.dataplatform.knmi.nl/open-data-api#token)

```{code-cell} ipython3
import requests
import datetime
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

#
# looks like "begin" and "end" don't do anything -- it just gets all filenames
#
timestamp_begin = datetime.date(2010,1,1).strftime("%Y-%m-%dT%H:%M:%S+00:00")
timestamp_end = datetime.date(2010,4,1).strftime("%Y-%m-%dT%H:%M:%S+00:00")
print(f"{timestamp_begin}")
params = {
    'maxKeys': '10',
    'sorting': 'desc',
    'orderBy': 'filename',
    'begin' : timestamp_begin
}

url = 'https://api.dataplatform.knmi.nl/open-data/v1/datasets/cesar_tower_meteo_lb1_t10/versions/v1.2/files'

response = requests.get(
    url,
    params=params,
    headers=headers,
)
out = response.json()
for the_file in out["files"]:
    print(the_file.get("filename"))
```

## Get the download url

Once you know the filename, download it into a tempory file and
rename it

```{code-cell} ipython3
filename = "cesar_tower_meteo_lb1_t10_v1.2_200005.nc"
part1 = 'https://api.dataplatform.knmi.nl/open-data/v1/datasets/'
part2 = f'cesar_tower_meteo_lb1_t10/versions/v1.2/files/{filename}/url'
url = part1 + part2
print(url)
response = requests.get(
    url,
    params=params,
    headers=headers,
)
out = response.json()
download_url = out["temporaryDownloadUrl"]
```

## Read the file into a local version

```{code-cell} ipython3
filename = "tower2_test.nc"
try:
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
except Exception:
    logger.exception("Unable to download file using download URL")
    sys.exit(1)
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
