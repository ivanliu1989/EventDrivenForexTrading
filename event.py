# -*- coding: utf-8 -*-

class Event(object):
    pass


class TickEvent(Event):
    ''' Instrument market data such as the (best) bid/ask 
    and the trade time'''
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask
        
        
class OrderEvent(Event):
    ''' Used to transmit orders to the execution handler
    Contains the instrument, the number of units to trader, 
    the order type and the side'''
    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type # market or limit
        self.side = side # buy and sell