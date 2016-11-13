# -*- coding: utf-8 -*-

from __future__ import print_function

from backtest.backtest import Backtest
from execution.execution import SimulatedExecution
from portfolio.portfolio import Portfolio
import settings
from strategy.strategy import MovingAverageCrossStrategy
from data.price import HistoricCSVPriceHandler


if __name__ == "__main__":
    # Trade on GBP/USD and EUR/USD
    pairs = ["GBPUSD", "EURUSD"]
    
    # Create the strategy parameters for the
    # MovingAverageCrossStrategy
    strategy_params = {
        "short_window": 500, 
        "long_window": 2000
    }
   
    # Create and execute the backtest
    backtest = Backtest(
        pairs, HistoricCSVPriceHandler, 
        MovingAverageCrossStrategy, strategy_params, 
        Portfolio, SimulatedExecution, 
        equity=settings.EQUITY
    )
    backtest.simulate_trading()