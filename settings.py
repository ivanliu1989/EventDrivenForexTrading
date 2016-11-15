# -*- coding: utf-8 -*-

from decimal import Decimal
import os


ENVIRONMENTS = { 
    "streaming": {
        "real": "stream-fxtrade.oanda.com",
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "real": "api-fxtrade.oanda.com",
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

CSV_DATA_DIR = 'C:\\Users\\sky_x\\Google Drive\\1. Work In Progress\\Git Projects\\Datasets\\'
OUTPUT_RESULTS_DIR = 'C:\\Users\\sky_x\\Google Drive\\1. Work In Progress\\Git Projects\\EventDrivenForexTrading\\Output\\'

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = '450188cd62d103f23afbbee7e72b1339-d9c47c032f04ff46a65ec24786d11357'
ACCOUNT_ID = '101-011-4686012-001'


BASE_CURRENCY = "AUD"
EQUITY = Decimal("1000000.00")