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

(sarima_co2)=
# SARIMA-TimeSeries Analysis of Atmospheric CO2

This notebook is replicated from the blog https://www.digitalocean.com/community/tutorials/a-guide-to-time-series-forecasting-with-arima-in-python-3 This tutorial will require the warnings, itertools, pandas, numpy, matplotlib and statsmodels libraries. The warnings and itertools libraries come included with the standard Python library set so we shouldn't need to install them.

In this tutorial, we will aim to produce reliable forecasts of time series. We will begin by introducing and discussing the concepts of autocorrelation, stationarity, and seasonality, and proceed to apply one of the most commonly used method for time-series forecasting, known as ARIMA.

One of the methods available in Python to model and predict future points of a time series is known as **SARIMAX**, which stands for **Seasonal AutoRegressive Integrated Moving Averages with eXogenous regressors**. Here, we will primarily focus on the ARIMA component, which is used to fit time-series data to better understand and forecast future points in the time series.

```{code-cell} ipython3
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.api as smt
import statsmodels.formula.api as smf
import scipy.stats as scs
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
```

## Step 1 - Loading Time-series Data

+++

We'll be working with a dataset called "Atmospheric CO2 from Continuous Air Samples at Mauna Loa Observatory, Hawaii, U.S.A.," which collected CO2 samples from March 1958 to December 2001. We can bring in this data as follows:

```{code-cell} ipython3
data = sm.datasets.co2.load_pandas()
df = data.data
df.head(5)
```

Let's preprocess our data a little bit before moving forward. Weekly data can be tricky to work with since it’s a briefer amount of time, so let's use monthly averages instead. We’ll make the conversion with the *resample* function. For simplicity, we can also use the *fillna()* function to ensure that we have no missing values in our time series.

```{code-cell} ipython3
# The 'MS' string groups the data in buckets by start of the month
ts = df['co2'].resample('MS').mean()
ts.head(5)
```

## Step 2 - Indexing with Time-series Data

```{code-cell} ipython3
ts.index
```

With our data properly indexed for working with temporal data, we can move onto handling values that may be missing.

## Step 3 - Handling Missing Values in Time-series Data

Real world data tends be messy. As we can see from the plot, it is not uncommon for time-series data to contain missing values. The simplest way to check for those is either by directly plotting the data or by using the command below that will reveal missing data.

```{code-cell} ipython3
ts.isnull().sum()
```

This output tells us that there are 5 months with missing values in our time series.

Generally, we should "fill in" missing values if they are not too numerous so that we don’t have gaps in the data. We can do this in pandas using the *fillna()* command. For simplicity, we can fill in missing values with the closest non-null value in our time series, although it is important to note that a rolling mean would sometimes be preferable.

```{code-cell} ipython3
# The term bfill means that we use the value before filling in missing values
ts = ts.fillna(ts.bfill())
ts.head(5)
```

With missing values filled in, we can once again check to see whether any null values exist to make sure that our operation worked:

```{code-cell} ipython3
ts.isnull().sum()
```

After performing these operations, we see that we have successfully filled in all missing values in our time series.

## Step 4 - Visualizing Time-series Data

When working with time-series data, a lot can be revealed through visualizing it. A few things to look out for are:

+ **seasonality:** does the data display a clear periodic pattern?
+ **trend:** does the data follow a consistent upwards or downward slope?
+ **noise:** are there any outlier points or missing values that are not consistent with the rest of the data?

```{code-cell} ipython3
plt.close()
ts.plot(figsize=(10, 6))
plt.show()
```

Some distinguishable patterns appear when we plot the data. The time-series has an obvious seasonality pattern, as well as an overall increasing trend. We can also visualize our data using a method called time-series decomposition. As its name suggests, time series decomposition allows us to decompose our time series into three distinct components: trend, seasonality, and noise.

Fortunately, *statsmodels* provides the convenient *seasonal_decompose* function to perform seasonal decomposition out of the box.

```{code-cell} ipython3
decomposition = sm.tsa.seasonal_decompose(ts, model='additive')
```

```{code-cell} ipython3
from pylab import rcParams
#rcParams['figure.figsize'] = 12, 10
fig = decomposition.plot()
fig.set_figwidth(12)
fig.set_figheight(8)
plt.show()
```

Using time-series decomposition makes it easier to quickly identify a changing mean or variation in the data. The plot above clearly shows the upwards trend of our data, along with its yearly seasonality. These can be used to understand the structure of our time-series. The intuition behind time-series decomposition is important, as many forecasting methods build upon this concept of structured decomposition to produce forecasts.

+++

## Step 5 - The ARIMA Time Series Model
One of the most common methods used in time series forecasting is known as the ARIMA model, which stands for **A**uto**R**egressive **I**ntegrated **M**oving **A**verage. ARIMA is a model that can be fitted to time series data in order to better understand or predict future points in the series.

There are three distinct integers (p, d, q) that are used to parametrize ARIMA models. Because of that, ARIMA models are denoted with the notation ARIMA(p, d, q). Together these three parameters account for seasonality, trend, and noise in datasets:

+ **p** is the *auto-regressive* part of the model. It allows us to incorporate the effect of past values into our model. Intuitively, this would be similar to stating that it is likely to be warm tomorrow if it has been warm the past 3 days.


+ **d** is the *integrated* part of the model. This includes terms in the model that incorporate the amount of differencing (i.e. the number of past time points to subtract from the current value) to apply to the time series. Intuitively, this would be similar to stating that it is likely to be same temperature tomorrow if the difference in temperature in the last three days has been very small.


+ **q** is the *moving average* part of the model. This allows us to set the error of our model as a linear combination of the error values observed at previous time points in the past.

When dealing with seasonal effects, we make use of the seasonal ARIMA, which is denoted as ARIMA(p,d,q)(P,D,Q)s. Here, (p, d, q) are the non-seasonal parameters described above, while (P, D, Q) follow the same definition but are applied to the seasonal component of the time series. The term s is the periodicity of the time series (4 for quarterly periods, 12 for yearly periods, etc.).

+++

## Step 6 - Parameter Selection for the ARIMA Time Series Model

When looking to fit time series data with a seasonal ARIMA model, our first goal is to find the values of ARIMA(p,d,q)(P,D,Q)s that optimize a metric of interest. There are many guidelines and best practices to achieve this goal, yet the correct parametrization of ARIMA models can be a painstaking manual process that requires domain expertise and time. Other statistical programming languages such as R provide automated ways to solve this issue, but those have yet to be ported over to Python. In this section, we will resolve this issue by writing Python code to programmatically select the optimal parameter values for our ARIMA(p,d,q)(P,D,Q)s time series model.

We will use a "grid search" to iteratively explore different combinations of parameters. For each combination of parameters, we fit a new seasonal ARIMA model with the SARIMAX() function from the statsmodels module and assess its overall quality. Once we have explored the entire landscape of parameters, our optimal set of parameters will be the one that yields the best performance for our criteria of interest. Let's begin by generating the various combination of parameters that we wish to assess:

```{code-cell} ipython3
# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, d and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
```

We can now use the triplets of parameters defined above to automate the process of training and evaluating ARIMA models on different combinations. In Statistics and Machine Learning, this process is known as grid search (or hyperparameter optimization) for model selection.

When evaluating and comparing statistical models fitted with different parameters, each can be ranked against one another based on how well it fits the data or its ability to accurately predict future data points. We will use the AIC (Akaike Information Criterion) value, which is conveniently returned with ARIMA models fitted using statsmodels. The AIC measures how well a model fits the data while taking into account the overall complexity of the model. A model that fits the data very well while using lots of features will be assigned a larger AIC score than a model that uses fewer features to achieve the same goodness-of-fit. Therefore, we are interested in finding the model that yields the lowest AIC value.

The code chunk below iterates through combinations of parameters and uses the SARIMAX function from statsmodels to fit the corresponding Seasonal ARIMA model. Here, the order argument specifies the (p, d, q) parameters, while the seasonal_order argument specifies the (P, D, Q, S) seasonal component of the Seasonal ARIMA model. After fitting each SARIMAX()model, the code prints out its respective AIC score.

```{code-cell} ipython3
warnings.filterwarnings("ignore") # specify to ignore warning messages

best_aic = np.inf
best_pdq = None
best_seasonal_pdq = None

for param in pdq:
    for param_seasonal in seasonal_pdq:
        
        try:
            model = sm.tsa.statespace.SARIMAX(ts,
                                             order = param,
                                             seasonal_order = param_seasonal,
                                             enforce_stationarity=False,
                                             enforce_invertibility=False)
            results = model.fit()

            # print("SARIMAX{}x{}12 - AIC:{}".format(param, param_seasonal, results.aic))
            if results.aic < best_aic:
                best_aic = results.aic
                best_pdq = param
                best_seasonal_pdq = param_seasonal
        except:
            continue
print("Best SARIMAX{}x{}12 model - AIC:{}".format(best_pdq, best_seasonal_pdq, best_aic))
```

+++ {"jupyter": {"outputs_hidden": true}}

Because some parameter combinations may lead to numerical misspecifications, we explicitly disabled warning messages in order to avoid an overload of warning messages. These misspecifications can also lead to errors and throw an exception, so we make sure to catch these exceptions and ignore the parameter combinations that cause these issues.

The output of our code suggests that SARIMAX(1, 1, 1)x(1, 1, 1, 12) yields the lowest AIC value of 277.78. We should therefore consider this to be optimal option out of all the models we have considered.

+++

## Step 5 — Fitting an ARIMA Time Series Model

Using grid search, we have identified the set of parameters that produces the best fitting model to our time series data. We can proceed to analyze this particular model in more depth.

We'll start by plugging the optimal parameter values into a new SARIMAX model:

```{code-cell} ipython3
best_model = sm.tsa.statespace.SARIMAX(ts,
                                      order=(1, 1, 1),
                                      seasonal_order=(1, 1, 1, 12),
                                      enforce_stationarity=False,
                                      enforce_invertibility=False)
results = best_model.fit()
```

```{code-cell} ipython3
print(results.summary().tables[0])
print(results.summary().tables[1])
```

The summary attribute that results from the output of SARIMAX returns a significant amount of information, but we'll focus our attention on the table of coefficients. The coef column shows the weight (i.e. importance) of each feature and how each one impacts the time series. The P>|z| column informs us of the significance of each feature weight. Here, each weight has a p-value lower or close to 0.05, so it is reasonable to retain all of them in our model.

When fitting seasonal ARIMA models (and any other models for that matter), it is important to run model diagnostics to ensure that none of the assumptions made by the model have been violated. The plot_diagnostics object allows us to quickly generate model diagnostics and investigate for any unusual behavior.

```{code-cell} ipython3
results.plot_diagnostics(figsize=(15,12))
plt.show()
```

Our primary concern is to ensure that the residuals of our model are uncorrelated and normally distributed with zero-mean. If the seasonal ARIMA model does not satisfy these properties, it is a good indication that it can be further improved.

In this case, our model diagnostics suggests that the model residuals are normally distributed based on the following:

+ In the top right plot, we see that the red KDE line follows closely with the N(0,1) line (where N(0,1)) is the standard notation for a normal distribution with mean 0 and standard deviation of 1). This is a good indication that the residuals are normally distributed.

+ The qq-plot on the bottom left shows that the ordered distribution of residuals (blue dots) follows the linear trend of the samples taken from a standard normal distribution with N(0, 1). Again, this is a strong indication that the residuals are normally distributed.

+ The residuals over time (top left plot) don't display any obvious seasonality and appear to be white noise. This is confirmed by the autocorrelation (i.e. correlogram) plot on the bottom right, which shows that the time series residuals have low correlation with lagged versions of itself.

Those observations lead us to conclude that our model produces a satisfactory fit that could help us understand our time series data and forecast future values.

Although we have a satisfactory fit, some parameters of our seasonal ARIMA model could be changed to improve our model fit. For example, our grid search only considered a restricted set of parameter combinations, so we may find better models if we widened the grid search.

+++

## Step 6 - Validating Forecasts

We have obtained a model for our time series that can now be used to produce forecasts. We start by comparing predicted values to real values of the time series, which will help us understand the accuracy of our forecasts. The get_prediction() and conf_int() attributes allow us to obtain the values and associated confidence intervals for forecasts of the time series.

```{code-cell} ipython3
pred = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=False)
pred_ci = pred.conf_int()
```

```{code-cell} ipython3
pred_ci.head(5)
```

The code above requires the forecasts to start at January 1998.

The dynamic=False argument ensures that we produce one-step ahead forecasts, meaning that forecasts at each point are generated using the full history up to that point.

We can plot the real and forecasted values of the CO<sub>2</sub> time series to assess how well we did. Notice how we zoomed in on the end of the time series by slicing the date index.

```{code-cell} ipython3
plt.close()
axis = ts['1990':].plot(figsize=(10, 6))
pred.predicted_mean.plot(ax=axis, label='One-step ahead Forecast', alpha=0.7)
axis.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.25)
axis.set_xlabel('Date')
axis.set_ylabel('CO2 Levels')
plt.legend(loc='best')
plt.show()
```

Overall, our forecasts align with the true values very well, showing an overall increase trend.

It is also useful to quantify the accuracy of our forecasts. We will use the MSE (Mean Squared Error), which summarizes the average error of our forecasts. For each predicted value, we compute its distance to the true value and square the result. The results need to be squared so that positive/negative differences do not cancel each other out when we compute the overall mean.

```{code-cell} ipython3
ts_forecasted = pred.predicted_mean
ts_truth = ts['1998-01-01':]

# Compute the mean sqaure error
mse = ((ts_forecasted - ts_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
```

The MSE of our one-step ahead forecasts yields a value of 0.07, which is very low as it is close to 0. An MSE of 0 would that the estimator is predicting observations of the parameter with perfect accuracy, which would be an ideal scenario but it not typically possible.

However, a better representation of our true predictive power can be obtained using dynamic forecasts. In this case, we only use information from the time series up to a certain point, and after that, forecasts are generated using values from previous forecasted time points.

In the code chunk below, we specify to start computing the dynamic forecasts and confidence intervals from January 1998 onwards.

```{code-cell} ipython3
pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=True, full_results=True)
pred_dynami_ci = pred_dynamic.conf_int()
```

Plotting the observed and forecasted values of the time series, we see that the overall forecasts are accurate even when using dynamic forecasts. All forecasted values (red line) match pretty closely to the ground truth (blue line), and are well within the confidence intervals of our forecast.

```{code-cell} ipython3
axis = ts['1990':].plot(label='Observed', figsize=(10, 6))
pred_dynamic.predicted_mean.plot(ax=axis, label='Dynamic Forecast', alpha=0.7)
axis.fill_between(pred_dynami_ci.index, pred_dynami_ci.iloc[:, 0], pred_dynami_ci.iloc[:, 1], color='k', alpha=.25)
axis.fill_betweenx(axis.get_ylim(), pd.to_datetime('1998-01-01'), ts.index[-1], alpha=.1, zorder=-1)
axis.set_xlabel('Date')
axis.set_ylabel('CO2 Levels')
plt.legend(loc='best')
plt.show()
plt.close()
```

Once again, we quantify the predictive performance of our forecasts by computing the MSE:

```{code-cell} ipython3
# Extract the predicted and true values of our time series
ts_forecasted = pred_dynamic.predicted_mean
ts_truth = ts['1998-01-01':]

# Compute the mean square error
mse = ((ts_forecasted - ts_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
```

The predicted values obtained from the dynamic forecasts yield an MSE of 1.01. This is slightly higher than the one-step ahead, which is to be expected given that we are relying on less historical data from the time series.

Both the one-step ahead and dynamic forecasts confirm that this time series model is valid. However, much of the interest around time series forecasting is the ability to forecast future values way ahead in time.

+++

## Step 7 - Producing and Visualizing Forecasts

In the final step of this tutorial, we describe how to leverage our seasonal ARIMA time series model to forecast future values. The get_forecast() attribute of our time series object can compute forecasted values for a specified number of steps ahead.

```{code-cell} ipython3
# Get forecast 500 steps ahead in future
n_steps = 500
pred_uc_99 = results.get_forecast(steps=500, alpha=0.01) # alpha=0.01 signifies 99% confidence interval
pred_uc_95 = results.get_forecast(steps=500, alpha=0.05) # alpha=0.05 95% CI

# Get confidence intervals of forecasts
pred_ci_99 = pred_uc_99.conf_int()
pred_ci_95 = pred_uc_95.conf_int()
```

```{code-cell} ipython3
n_steps = 500
idx = pd.date_range(ts.index[-1], periods=n_steps, freq='MS')
fc_95 = pd.DataFrame(np.column_stack([pred_uc_95.predicted_mean, pred_ci_95]), 
                     index=idx, columns=['forecast', 'lower_ci_95', 'upper_ci_95'])
fc_99 = pd.DataFrame(np.column_stack([pred_ci_99]), 
                     index=idx, columns=['lower_ci_99', 'upper_ci_99'])
fc_all = fc_95.combine_first(fc_99)
fc_all.head()
```

We can use the output of this code to plot the time series and forecasts of its future values.

```{code-cell} ipython3
plt.close()
axis = ts.plot(label='Observed', figsize=(15, 6))
pred_uc_95.predicted_mean.plot(ax=axis, label='Forecast', alpha=0.7)
axis.fill_between(pred_ci_95.index, pred_ci_95.iloc[:, 0], pred_ci_95.iloc[:, 1], color='k', alpha=.25)
#axis.fill_between(pred_ci_99.index, pred_ci_99.iloc[:, 0], pred_ci_99.iloc[:, 1], color='b', alpha=.25)
axis.set_xlabel('Date')
axis.set_ylabel('CO2 Levels')
plt.legend(loc='best')
plt.show()
```

Both the forecasts and associated confidence interval that we have generated can now be used to further understand the time series and foresee what to expect. Our forecasts show that the time series is expected to continue increasing at a steady pace.

As we forecast further out into the future, it is natural for us to become less confident in our values. This is reflected by the confidence intervals generated by our model, which grow larger as we move further out into the future.
