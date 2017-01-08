import oandaInstrument as oi
import pandas as pd
import numpy as np
# import rpy2.robjects as robjects

#Write a function to compare the imported python df and the R df.

#----Retrive data from Oanda API
oandaDict = oi.initiateOandaDict()
AUD_USD = oi.getOandaInstrumentCandles(oanda = oandaDict,
    INSTRUMENTS = 'AUD_USD', price = "M", granularity = "D", count = "300")
AUD_USD.columns = ["Complete", "Close", "High", "Low", "Open", "time", "Volume"]
spReturns = AUD_USD.loc[:,['time','Close']]
spReturns.loc[:,'Close'] = pd.to_numeric(spReturns.loc[:,'Close'])
spReturns.loc[:,'time'] = pd.to_datetime(spReturns.loc[:,'time'])
value = np.diff(np.log(spReturns.loc[:,'Close']))
spReturns.loc[:,'Close'] = np.insert(value, 0, 0) #insert 0 to top row

#-----Prepare R xts object (function call from R library)--------
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
pandas2ri.activate() #activate two-way autoconversion of pandas df <--> R df
xts = importr("xts", robject_translations = {".subset.xts": "_subset_xts2",
                                             "to.period": "to_period2"})
r_base = importr('base')
spReturns = xts.xts(spReturns.Close,
    r_base.as_POSIXct(r_base.as_Date(spReturns.time)))

#-----Call R function (function call from .R file)-----
from rpy2.robjects.packages import STAP
with open(r'C:\morelia\anz_ds\Algorithmic_Trading_System\RQuantTrader\tests\ARIMIA_GARCH.R', 'r') as f:
    rstring = f.read()
r_AG = STAP(rstring, 'r_AG')
res = r_AG.ARIMA_GARCH_IN_R(spReturns) #return <class 'rpy2.robjects.vectors.DataFrame'>
print(res)
