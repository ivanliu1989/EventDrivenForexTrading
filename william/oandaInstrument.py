import pandas as pd
import requests

def initiateOandaDict():
    oandaEnv = dict(
        ACCESS_TOKEN = "450188cd62d103f23afbbee7e72b1339-d9c47c032f04ff46a65ec24786d11357",
        ACCOUNT_ID = "101-011-4686012-003",
        ACCOUNT_TYPE = "practice",
        ENVIRONMENTS = dict(
            streaming = dict(
                real = "stream-fxtrade.oanda.com",
                practice = "stream-fxpractice.oanda.com",
                sandbox = "stream-sandbox.oanda.com"
            ),
            api = dict(
                real = "api-fxtrade.oanda.com",
                practice = "api-fxpractice.oanda.com",
                sandbox = "api-sandbox.oanda.com"
            )
        ),
        INIT_AMOUNT = 1000000,
        RISK_MANAGEMENT = 0.02
    )
    oandaEnv['STREAM_DOMAIN'] = oandaEnv['ENVIRONMENTS']['streaming'][oandaEnv['ACCOUNT_TYPE']]
    oandaEnv['API_DOMAIN'] = oandaEnv['ENVIRONMENTS']['api'][oandaEnv['ACCOUNT_TYPE']]
    return(oandaEnv)

def getOandaInstrumentCandles(oanda, INSTRUMENTS = 'AUD_USD',
    price = "M", granularity = "D", **kwargs):

    # Must
    price = "price=" + price
    granularity = "granularity=" + granularity
    QUERY = price + "&" + granularity

    if 'count' in kwargs: count = "count=" + kwargs.get('count'); QUERY = QUERY + "&" + count

    # Optional1
    if 'from' in kwargs: froms = "from=" + kwargs.get('from'); QUERY = QUERY + "&" + froms
    if 'to' in kwargs: to = "to=" + kwargs.get('to'); QUERY = QUERY + "&" + to

    # Optional2
    if 'smooth.param' in kwargs: smooth.param = "smooth="+kwargs.get('smooth.param'); QUERY = QUERY + "&" + smooth.param
    if 'includeFirst' in kwargs: includeFirst = "includeFirst="+kwargs.get('includeFirst'); QUERY = QUERY + "&" + includeFirst
    if 'dailyAlignment' in kwargs: dailyAlignment = "dailyAlignment="+kwargs.get('dailyAlignment'); QUERY = QUERY + "&" + dailyAlignment
    if 'alignmentTimezone' in kwargs: alignmentTimezone = "alignmentTimezone="+kwargs.get('alignmentTimezone'); QUERY = QUERY + "&" + alignmentTimezone
    if 'weeklyAlignment' in kwargs: weeklyAlignment = "weeklyAlignment="+kwargs.get('weeklyAlignment'); QUERY = QUERY + "&" + weeklyAlignment

    # Generate URL ------------------------------------------------------------
    URL = "https://" + oanda.get('API_DOMAIN') + "/v3/instruments/" + INSTRUMENTS + "/candles?"
    URL = URL + QUERY

     # Headers -----------------------------------------------------------------
    HEADERS = {
        'Authorization' : "Bearer" + " " + oanda.get('ACCESS_TOKEN'),
        'Content-Type' : "application/x-www-form-urlencoded"
        }
    r = requests.get(URL, headers = HEADERS) #may change to change **HEADERS if there is error
    if r.status_code == requests.codes.ok:
        data = r.json()['candles'] #r.json() is a dict
        df = pd.io.json.json_normalize(data) #translate json dict to df
    else:
        print ('getOandaInstrumentCandles():' + r.raise_for_status())
    return(df)

# oandaEnv = initiateOandaEnv()
# df = getOandaInstrumentCandles(oanda = oandaEnv)
# print(df)
