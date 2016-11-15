# -*- coding: utf-8 -*-
from __future__ import print_function

from abc import ABCMeta, abstractmethod
try:
    import httplib
except ImportError:
    import http.client as httplib
import logging
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import urllib3
urllib3.disable_warnings()
import json
import requests


class ExecutionHandler(object):
    """
    Provides an abstract base class to handle all execution in the
    backtesting and live trading system.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute_order(self):
        """
        Send the order to the brokerage.
        """
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecution(object):
    """
    Provides a simulated execution handling environment. This class
    actually does nothing - it simply receives an order to execute.
    Instead, the Portfolio object actually provides fill handling.
    This will be modified in later versions.
    """
    def execute_order(self, event):
        pass


class OANDAExecutionHandler(ExecutionHandler):
    def __init__(self, domain, access_token, account_id):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.conn = self.obtain_connection()
        self.logger = logging.getLogger(__name__)

    def obtain_connection(self):
        return httplib.HTTPSConnection(self.domain)

    def execute_order(self, event):
        instrument = "%s_%s" % (event.instrument[:3], event.instrument[3:])
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }
        if event.side == 'BUY':
            units = event.units
        else:
            units = -event.units
        params = json.dumps(
            {"order": {
                "units": str(units), 
                "instrument": instrument, 
                "timeInForce": "FOK", 
                "type": "MARKET",#event.order_type, 
                "positionFill": "DEFAULT",
                "side": event.side
              }
        })
        print(params)
        url = 'https://' + self.domain + '/v3/accounts/' + self.account_id + '/orders'
        
        response = requests.post(url, data=params, headers=headers)
        self.logger.debug(response)
        
        