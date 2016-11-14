# -*- coding: utf-8 -*-


from OandaAPI import OandaApi

    
if __name__ == '__main__':
    token = '450188cd62d103f23afbbee7e72b1339-d9c47c032f04ff46a65ec24786d11357'
    accountId = '101-011-4686012-001'
    
    api = OandaApi()
    api.DEBUG = True
    
    api.init('practice', token, accountId)
    #api.processStreamPrices()
    
    # 获取交易合约列表，通过
    api.getInstruments({'accountId': accountId})
    
    # 获取价格，通过
#    while 1:
    api.getPrices({'instruments': 'AUD_USD'})
    
    # 获取历史数据，失败
    api.getPriceHisory('EUR_USD',{'instrument': 'EUR_USD',
                        'granularity': 'D',
                        'candleFormat': 'midpoint',
                        'count': '50'})
    
    # 查询用户的所有账户，通过
    api.getAccounts()
    
    # 查询账户信息，通过
    api.getAccountInfo()
    
    # 查询委托数据，通过
    api.getOrders({})
    
    # 发送委托，通过
    api.sendOrder({'instrument': 'AUD_USD',
                   'units': '1000000',
                   'price': '1.2000',
                   'type': 'MARKET'})
#    
    # 查询委托数据，通过
    #api.getOrderInfo('123')
    
    # 修改委托，通过
#    api.modifyOrder({'units': '10000',
#                   'side': 'buy',
#                   'type': 'MARKET'}, '123')    
    
    # 撤销委托，通过
    #api.cancelOrder('123')
    
    # 查询所有持仓，通过
    #api.getTrades({})
    
    # 查询持仓数据，通过
    #api.getTradeInfo('10125150909')
    
    # 修改持仓，通过
    #api.modifyTrade({'trailingStop': '150'}, '10125150909')    
    
    # 平仓，通过
    #api.closeTrade('10125150909')   
    
    # 查询汇总持仓，通过
    #api.getPositions()
    
    # 查询汇总持仓细节，通过
    #api.getPositionInfo('AUD_USD')
    
    # 平仓汇总持仓，通过
    #api.closePosition('EUR_USD')
    
    # 查询账户资金变动，通过
    #api.getTransactions({})
    
    # 查询资金变动信息，通过
    #api.getTransactionInfo('10135713982')
    
    # 查询账户变动历史，部分通过，某些情况下可能触发JSONDecodeError
    #api.getAccountHistory()
    
    # 查询财经日历，通过
    #api.getCalendar({'period': '604800'})
    
    # 查询历史持仓比，通过
    #api.getPositionRatios({'instrument': 'EUR_USD',
                           #'period': '604800'})
    
    # 查询历史价差，通过
    #api.getSpreads({'instrument': 'EUR_USD',
                    #'period': '604800'})
    
    # 查询交易商持仓，通过
    #api.getCommitments({'instrument': 'EUR_USD'})
    
    # 查询订单簿，通过
    #api.getOrderbook({'instrument': 'EUR_USD',
                      #'period': '604800'})
    
    # 查询Autochartist，失败，OANDA服务器报错
    #api.getAutochartist({'instrument': 'EUR_USD'})
    
    # 阻塞
    input()    
