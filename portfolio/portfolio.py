# -*- coding: utf-8 -*-
from copy import deepcopy

from event.event import OrderEvent
from position import Position


class Portfolio(object): 

    def __init__(
        self, ticker, events, base="GBP", leverage=20, 
        equity=100000.0, risk_per_trade=0.02
    ):
        self.ticker = ticker # the streaming forex prices ticker handler. lastest bid/ask prices
        self.events = events # order events
        self.base = base # base currency
        self.leverage = leverage # leverage 1:20
        self.equity = equity 
        self.balance = deepcopy(self.equity)
        self.risk_per_trade = risk_per_trade # % of acc equity to risk per trade
        self.trade_units = self.calc_risk_position_size()
        self.positions = {}

    def calc_risk_position_size(self):
        return self.equity * self.risk_per_trade

    def add_new_position(
        self, side, market, units, exposure,
        add_price, remove_price
    ):
        # takes the parameters necessary to add a new position to the portfolio
        ps = Position(
            side, market, units, exposure,
            add_price, remove_price
        )
        self.positions[market] = ps

    def add_position_units(
        self, market, units, exposure, 
        add_price, remove_price
    ):
        # allows units to be added to a position once the position has been created
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            new_total_units = ps.units + units
            new_total_cost = ps.avg_price*ps.units + add_price*units
            ps.exposure += exposure
            ps.avg_price = new_total_cost/new_total_units
            ps.units = new_total_units
            ps.update_position_price(remove_price)
            return True

    def remove_position_units(
        self, market, units, remove_price
    ):
        # a method to remove the units from a position (but not to close it entirely)
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.units -= units
            exposure = float(units)
            ps.exposure -= exposure
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * exposure / remove_price 
            self.balance += pnl
            return True

    def close_position(
        self, market, remove_price
    ):
        # fully close a position
        if market not in self.positions:
            return False
        else:
            ps = self.positions[market]
            ps.update_position_price(remove_price)
            pnl = ps.calculate_pips() * ps.exposure / remove_price 
            self.balance += pnl
            del[self.positions[market]]
            return True

    def execute_signal(self, signal_event):
        #==============================================================================
        #     If there is no current position for this currency pair, create one.
        #     If a position already exists, check to see if it is adding or subtracting units.
        #     If it is adding units, then simply add the correct amount of units.
        #     If it is not adding units, then check if the new opposing unit reduction closes out the trade, if so, then do so.
        #     If the reducing units are less than the position units, simply remove that quantity from the position.
        #     However, if the reducing units exceed the current position, it is necessary to close the current position by the reducing units and 
        #     then create a new opposing position with the remaining units. I have not tested this extensively as of yet, so there may still be bugs!
        #==============================================================================
        side = signal_event.side
        market = signal_event.instrument
        units = int(self.trade_units)

        # Check side for correct bid/ask prices
        add_price = self.ticker.cur_ask
        remove_price = self.ticker.cur_bid
        exposure = float(units)

        # If there is no position, create one
        if market not in self.positions:
            self.add_new_position(
                side, market, units, exposure,
                add_price, remove_price
            )
            order = OrderEvent(market, units, "market", "buy")
            self.events.put(order)
        # If a position exists add or remove units
        else:
            ps = self.positions[market]
            # Check if the sides equal
            if side == ps.side:
                # Add to the position
                self.add_position_units(
                    market, units, exposure,
                    add_price, remove_price
                )
            else:
                # Check if the units close out the position
                if units == ps.units:
                    # Close the position
                    self.close_position(market, remove_price)
                    order = OrderEvent(market, units, "market", "sell")
                    self.events.put(order)
                elif units < ps.units:
                    # Remove from the position
                    self.remove_position_units(
                        market, units, remove_price
                    )
                else: # units > ps.units
                    # Close the position and add a new one with
                    # additional units of opposite side
                    new_units = units - ps.units
                    self.close_position(market, remove_price)
                    
                    if side == "buy":
                        new_side = "sell"
                    else:
                        new_side = "sell"
                    new_exposure = float(units)
                    self.add_new_position(
                        new_side, market, new_units, 
                        new_exposure, add_price, remove_price
                    )
        print "Balance: %0.2f" % self.balance