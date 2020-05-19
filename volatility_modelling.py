## set up ##

import numpy as np
import pandas as pd
import datetime as dt
import datapackage
from arch import arch_model
import matplotlib.pyplot as plt
import statsmodels.api as sm

## importing and cleaning data ##

url = 'https://raw.githubusercontent.com/joe-ascroft/phd/master/wti_hh.csv'
df = pd.read_csv(url)
df["DATE"] = pd.to_datetime(df["DATE"])
df["HH_P"] = pd.to_numeric(df["HH_P"],errors='coerce')
df["WTI_P"] = pd.to_numeric(df["WTI_P"],errors='coerce')

df = df.dropna()

## calculate daily price volatility ##

HH_vol = df["HH_P"].pct_change()
HH_vol = HH_vol.dropna()
print(HH_vol)

WTI_vol = df["WTI_P"].pct_change()
WTI_vol = WTI_vol.dropna()
print(WTI_vol)

## chart price volatility ##

plt.plot(df["DATE"][1:],WTI_vol)

## fit volatility model ##

am1 = arch_model(HH_vol)
res = am1.fit()
print(res.summary())





