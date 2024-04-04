---
jupytext:
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

(ma_model)=
# moving average model

```{code-cell} ipython3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
register_matplotlib_converters()
```

+++ {"jp-MarkdownHeadingCollapsed": true}

## Generate Some Data

+++

# $y_t = 50 + 0.4\varepsilon_{t-1} + 0.3\varepsilon_{t-2} + \varepsilon_t$
# $\varepsilon_t \sim N(0,1)$

```{code-cell} ipython3
errors = np.random.normal(0, 1, 400)
```

```{code-cell} ipython3
date_index = pd.date_range(start='9/1/2019', end='1/1/2020')
```

```{code-cell} ipython3
mu = 50
series = []
for t in range(1,len(date_index)+1):
    series.append(mu + 0.4*errors[t-1] + 0.3*errors[t-2] + errors[t])
```

## infer frequency for plotting

```{code-cell} ipython3
series = pd.Series(series, date_index)
series = series.asfreq(pd.infer_freq(series.index))
```

```{code-cell} ipython3
plt.figure(figsize=(10,4))
plt.plot(series)
plt.axhline(mu, linestyle='--', color='grey')
```

```{code-cell} ipython3
def calc_corr(series, lag):
    return pearsonr(series[:-lag], series[lag:])[0]
```

# autocorrelation function (ACF)

```{code-cell} ipython3
acf_vals = acf(series)
num_lags = 10
plt.bar(range(num_lags), acf_vals[:num_lags]);
```

# Partial auto-correlation function (PACF)

```{code-cell} ipython3
pacf_vals = pacf(series)
num_lags = 20
plt.bar(range(num_lags), pacf_vals[:num_lags]);
```

# Get training and testing sets

```{code-cell} ipython3
train_end = datetime(2019,12,30)
test_end = datetime(2020,1,1)

train_data = series[:train_end]
test_data = series[train_end + timedelta(days=1):test_end]
```

## Fit ARIMA Model as 2-lag MA model

```{code-cell} ipython3
#create the model
model = ARIMA(train_data, order=(0,0,2))
```

```{code-cell} ipython3
#fit the model
model_fit = model.fit()
```

```{code-cell} ipython3
#summary of the model
print(model_fit.summary())
```

## Predicted Model:

$\hat{y}_t = 50 + 0.37\varepsilon_{t-1} + 0.25\varepsilon_{t-2}$

```{code-cell} ipython3
#get prediction start and end dates
pred_start_date = test_data.index[0]
pred_end_date = test_data.index[-1]
```

```{code-cell} ipython3
#get the predictions and residuals
predictions = model_fit.predict(start=pred_start_date, end=pred_end_date)
```

```{code-cell} ipython3
residuals = test_data - predictions
```

```{code-cell} ipython3
plt.figure(figsize=(10,4))

plt.plot(series[-14:])
plt.plot(predictions)

plt.legend(('Data', 'Predictions'), fontsize=16)
```

```{code-cell} ipython3
print('Mean Absolute Percent Error:', round(np.mean(abs(residuals/test_data)),4))
```

```{code-cell} ipython3
print('Root Mean Squared Error:', np.sqrt(np.mean(residuals**2)))
```

```{code-cell} ipython3

```
