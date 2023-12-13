# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.base.types import Balances, Int, Order, OrderBook, Str, Ticker, Trade
from ccxt.async_support.base.ws.client import Client
from typing import List
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import AuthenticationError
from ccxt.base.precise import Precise


class whitebit(ccxt.async_support.whitebit):

    def describe(self):
        return self.deep_extend(super(whitebit, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchMyTrades': True,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchTicker': True,
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://api.whitebit.com/ws',
                },
            },
            'options': {
                'timeframes': {
                    '1m': '60',
                    '5m': '300',
                    '15m': '900',
                    '30m': '1800',
                    '1h': '3600',
                    '4h': '14400',
                    '8h': '28800',
                    '1d': '86400',
                    '1w': '604800',
                },
                'watchOrderBook': {
                    'priceInterval': 0,  # "0" - no interval, available values - "0.00000001", "0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.01", "0.1"
                },
            },
            'streaming': {
                'ping': self.ping,
            },
            'exceptions': {
                'ws': {
                    'exact': {
                        '1': BadRequest,  # {error: {code: 1, message: 'invalid argument'}, result: null, id: 1656404342}
                        '2': BadRequest,  # {error: {code: 2, message: 'internal error'}, result: null, id: 1656404075}
                        '4': BadRequest,  # {error: {code: 4, message: 'method not found'}, result: null, id: 1656404250}
                        '6': AuthenticationError,  # {error: {code: 6, message: 'require authentication'}, result: null, id: 1656404076}
                    },
                },
            },
        })

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Int = None, limit: Int = None, params={}) -> List[list]:
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        timeframes = self.safe_value(self.options, 'timeframes', {})
        interval = self.safe_integer(timeframes, timeframe)
        marketId = market['id']
        # currently there is no way of knowing
        # the interval upon getting an update
        # so that can't be part of the message hash, and the user can only subscribe
        # to one timeframe per symbol
        messageHash = 'candles:' + symbol
        reqParams = [marketId, interval]
        method = 'candles_subscribe'
        ohlcv = await self.watch_public(messageHash, method, reqParams, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client: Client, message):
        #
        # {
        #     "method": "candles_update",
        #     "params": [
        #       [
        #         1655204760,
        #         "22374.15",
        #         "22351.34",
        #         "22374.27",
        #         "22342.52",
        #         "30.213426",
        #         "675499.29718947",
        #         "BTC_USDT"
        #       ]
        #     ],
        #     "id": null
        # }
        #
        params = self.safe_value(message, 'params', [])
        for i in range(0, len(params)):
            data = params[i]
            marketId = self.safe_string(data, 7)
            market = self.safe_market(marketId)
            symbol = market['symbol']
            messageHash = 'candles' + ':' + symbol
            parsed = self.parse_ohlcv(data, market)
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol)
            stored = self.ohlcvs[symbol]
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol] = stored
            stored.append(parsed)
            client.resolve(stored, messageHash)
        return message

    async def watch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 10  # max 100
        messageHash = 'orderbook' + ':' + market['symbol']
        method = 'depth_subscribe'
        options = self.safe_value(self.options, 'watchOrderBook', {})
        defaultPriceInterval = self.safe_string(options, 'priceInterval', '0')
        priceInterval = self.safe_string(params, 'priceInterval', defaultPriceInterval)
        params = self.omit(params, 'priceInterval')
        reqParams = [
            market['id'],
            limit,
            priceInterval,
            True,  # True for allowing multiple subscriptions
        ]
        orderbook = await self.watch_public(messageHash, method, reqParams, params)
        return orderbook.limit()

    def handle_order_book(self, client: Client, message):
        #
        # {
        #     "method":"depth_update",
        #     "params":[
        #        True,
        #        {
        #           "asks":[
        #              ["21252.45","0.01957"],
        #              ["21252.55","0.126205"],
        #              ["21252.66","0.222689"],
        #              ["21252.76","0.185358"],
        #              ["21252.87","0.210077"],
        #              ["21252.98","0.303991"],
        #              ["21253.08","0.327909"],
        #              ["21253.19","0.399007"],
        #              ["21253.3","0.427695"],
        #              ["21253.4","0.492901"]
        #           ],
        #           "bids":[
        #              ["21248.82","0.22"],
        #              ["21248.73","0.000467"],
        #              ["21248.62","0.100864"],
        #              ["21248.51","0.061436"],
        #              ["21248.42","0.091"],
        #              ["21248.41","0.126839"],
        #              ["21248.3","0.063511"],
        #              ["21248.2","0.110547"],
        #              ["21248","0.25257"],
        #              ["21247.7","1.71813"]
        #           ]
        #        },
        #        "BTC_USDT"
        #     ],
        #     "id":null
        #  }
        #
        params = self.safe_value(message, 'params', [])
        isSnapshot = self.safe_value(params, 0)
        marketId = self.safe_string(params, 2)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        data = self.safe_value(params, 1)
        orderbook = None
        if symbol in self.orderbooks:
            orderbook = self.orderbooks[symbol]
        else:
            orderbook = self.order_book()
            self.orderbooks[symbol] = orderbook
        if isSnapshot:
            snapshot = self.parse_order_book(data, symbol)
            orderbook.reset(snapshot)
        else:
            asks = self.safe_value(data, 'asks', [])
            bids = self.safe_value(data, 'bids', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
        messageHash = 'orderbook' + ':' + symbol
        client.resolve(orderbook, messageHash)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    async def watch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        method = 'market_subscribe'
        messageHash = 'ticker:' + symbol
        # every time we want to subscribe to another market we have to "re-subscribe" sending it all again
        return await self.watch_multiple_subscription(messageHash, method, symbol, False, params)

    def handle_ticker(self, client: Client, message):
        #
        #   {
        #       "method": "market_update",
        #       "params": [
        #         "BTC_USDT",
        #         {
        #           "close": "22293.86",
        #           "deal": "1986990019.96552952",
        #           "high": "24360.7",
        #           "last": "22293.86",
        #           "low": "20851.44",
        #           "open": "24076.12",
        #           "period": 86400,
        #           "volume": "87016.995668"
        #         }
        #       ],
        #       "id": null
        #   }
        #
        tickers = self.safe_value(message, 'params', [])
        marketId = self.safe_string(tickers, 0)
        market = self.safe_market(marketId, None)
        symbol = market['symbol']
        rawTicker = self.safe_value(tickers, 1, {})
        messageHash = 'ticker' + ':' + symbol
        ticker = self.parse_ticker(rawTicker, market)
        self.tickers[symbol] = ticker
        # watchTicker
        client.resolve(ticker, messageHash)
        # watchTickers
        messageHashes = list(client.futures.keys())
        for i in range(0, len(messageHashes)):
            currentMessageHash = messageHashes[i]
            if currentMessageHash.find('tickers') >= 0 and currentMessageHash.find(symbol) >= 0:
                # Example: user calls watchTickers with ['LTC/USDT', 'ETH/USDT']
                # the associated messagehash will be: 'tickers:LTC/USDT:ETH/USDT'
                # since we only have access to a single symbol at a time
                # we have to do a reverse lookup into the tickers hashes
                # and check if the current symbol is a part of one or more
                # tickers hashes and resolve them
                # user might have multiple watchTickers promises
                # watchTickers( ['LTC/USDT', 'ETH/USDT'] ), watchTickers( ['ETC/USDT', 'DOGE/USDT'] )
                # and we want to make sure we resolve only the correct ones
                client.resolve(ticker, currentMessageHash)
        return message

    async def watch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = 'trades' + ':' + symbol
        method = 'trades_subscribe'
        # every time we want to subscribe to another market we have to 're-subscribe' sending it all again
        trades = await self.watch_multiple_subscription(messageHash, method, symbol, False, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client: Client, message):
        #
        #    {
        #        "method":"trades_update",
        #        "params":[
        #           "BTC_USDT",
        #           [
        #              {
        #                 "id":1900632398,
        #                 "time":1656320231.404343,
        #                 "price":"21443.04",
        #                 "amount":"0.072844",
        #                 "type":"buy"
        #              },
        #              {
        #                 "id":1900632397,
        #                 "time":1656320231.400001,
        #                 "price":"21443.15",
        #                 "amount":"0.060757",
        #                 "type":"buy"
        #              }
        #           ]
        #        ]
        #    }
        #
        params = self.safe_value(message, 'params', [])
        marketId = self.safe_string(params, 0)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        data = self.safe_value(params, 1, [])
        parsedTrades = self.parse_trades(data, market)
        for j in range(0, len(parsedTrades)):
            stored.append(parsedTrades[j])
        messageHash = 'trades:' + market['symbol']
        client.resolve(stored, messageHash)

    async def watch_my_trades(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        watches trades made by the user
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/#/?id=trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' watchMyTrades() requires a symbol argument')
        await self.load_markets()
        await self.authenticate()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = 'myTrades:' + symbol
        method = 'deals_subscribe'
        trades = await self.watch_multiple_subscription(messageHash, method, symbol, True, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_my_trades(self, client: Client, message, subscription=None):
        #
        #   {
        #       "method": "deals_update",
        #       "params": [
        #         1894994106,
        #         1656151427.729706,
        #         "LTC_USDT",
        #         96624037337,
        #         "56.78",
        #         "0.16717",
        #         "0.0094919126",
        #         ''
        #       ],
        #       "id": null
        #   }
        #
        trade = self.safe_value(message, 'params')
        if self.myTrades is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            self.myTrades = ArrayCache(limit)
        stored = self.myTrades
        parsed = self.parse_ws_trade(trade)
        stored.append(parsed)
        symbol = parsed['symbol']
        messageHash = 'myTrades:' + symbol
        client.resolve(stored, messageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        #   [
        #         1894994106,  # id
        #         1656151427.729706,  # deal time
        #         "LTC_USDT",  # symbol
        #         96624037337,  # order id
        #         "56.78",  # price
        #         "0.16717",  # amount
        #         "0.0094919126",  # fee
        #         ''  # client order id
        #    ]
        #
        orderId = self.safe_string(trade, 3)
        timestamp = self.safe_timestamp(trade, 1)
        id = self.safe_string(trade, 0)
        price = self.safe_string(trade, 4)
        amount = self.safe_string(trade, 5)
        marketId = self.safe_string(trade, 2)
        market = self.safe_market(marketId, market)
        fee = None
        feeCost = self.safe_string(trade, 6)
        if feeCost is not None:
            fee = {
                'cost': feeCost,
                'currency': market['quote'],
            }
        return self.safe_trade({
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': orderId,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': fee,
        }, market)

    async def watch_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        watches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of [order structures]{@link https://docs.ccxt.com/#/?id=order-structure
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' watchOrders() requires a symbol argument')
        await self.load_markets()
        await self.authenticate()
        market = self.market(symbol)
        symbol = market['symbol']
        messageHash = 'orders:' + symbol
        method = 'ordersPending_subscribe'
        trades = await self.watch_multiple_subscription(messageHash, method, symbol, False, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    def handle_order(self, client: Client, message, subscription=None):
        #
        # {
        #     "method": "ordersPending_update",
        #     "params": [
        #       1,  # 1 = new, 2 = update 3 = cancel or execute
        #       {
        #         "id": 96433622651,
        #         "market": "LTC_USDT",
        #         "type": 1,
        #         "side": 2,
        #         "ctime": 1656092215.39375,
        #         "mtime": 1656092215.39375,
        #         "price": "25",
        #         "amount": "0.202",
        #         "taker_fee": "0.001",
        #         "maker_fee": "0.001",
        #         "left": "0.202",
        #         "deal_stock": "0",
        #         "deal_money": "0",
        #         "deal_fee": "0",
        #         "client_order_id": ''
        #       }
        #     ]
        #     "id": null
        # }
        #
        params = self.safe_value(message, 'params', [])
        data = self.safe_value(params, 1)
        if self.orders is None:
            limit = self.safe_integer(self.options, 'ordersLimit', 1000)
            self.orders = ArrayCacheBySymbolById(limit)
        stored = self.orders
        status = self.safe_integer(params, 0)
        parsed = self.parse_ws_order(self.extend(data, {'status': status}))
        stored.append(parsed)
        symbol = parsed['symbol']
        messageHash = 'orders:' + symbol
        client.resolve(self.orders, messageHash)

    def parse_ws_order(self, order, market=None):
        #
        #   {
        #         "id": 96433622651,
        #         "market": "LTC_USDT",
        #         "type": 1,
        #         "side": 2,  #1- sell 2-buy
        #         "ctime": 1656092215.39375,
        #         "mtime": 1656092215.39375,
        #         "price": "25",
        #         "amount": "0.202",
        #         "taker_fee": "0.001",
        #         "maker_fee": "0.001",
        #         "left": "0.202",
        #         "deal_stock": "0",
        #         "deal_money": "0",
        #         "deal_fee": "0",
        #         "activation_price": "40",
        #         "activation_condition": "lte",
        #         "client_order_id": ''
        #         "status": 1,  # 1 = new, 2 = update 3 = cancel or execute
        #    }
        #
        status = self.safe_integer(order, 'status')
        marketId = self.safe_string(order, 'market')
        market = self.safe_market(marketId, market)
        id = self.safe_string(order, 'id')
        clientOrderId = self.omit_zero(self.safe_string(order, 'client_order_id'))
        price = self.safe_string(order, 'price')
        filled = self.safe_string(order, 'deal_stock')
        cost = self.safe_string(order, 'deal_money')
        stopPrice = self.safe_string(order, 'activation_price')
        rawType = self.safe_string(order, 'type')
        type = self.parse_ws_order_type(rawType)
        amount = None
        remaining = None
        if type == 'market':
            amount = self.safe_string(order, 'deal_stock')
            remaining = '0'
        else:
            remaining = self.safe_string(order, 'left')
            amount = self.safe_string(order, 'amount')
        timestamp = self.safe_timestamp(order, 'ctime')
        lastTradeTimestamp = self.safe_timestamp(order, 'mtime')
        symbol = market['symbol']
        rawSide = self.safe_integer(order, 'side')
        side = 'sell' if (rawSide == 1) else 'buy'
        dealFee = self.safe_string(order, 'deal_fee')
        fee = None
        if dealFee is not None:
            fee = {
                'cost': self.parse_number(dealFee),
                'currency': market['quote'],
            }
        unifiedStatus = None
        if (status == 1) or (status == 2):
            unifiedStatus = 'open'
        else:
            if Precise.string_equals(remaining, '0'):
                unifiedStatus = 'closed'
            else:
                unifiedStatus = 'canceled'
        return self.safe_order({
            'info': order,
            'symbol': symbol,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'type': type,
            'timeInForce': None,
            'postOnly': None,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'triggerPrice': stopPrice,
            'amount': amount,
            'cost': cost,
            'average': None,
            'filled': filled,
            'remaining': remaining,
            'status': unifiedStatus,
            'fee': fee,
            'trades': None,
        }, market)

    def parse_ws_order_type(self, status):
        statuses = {
            '1': 'limit',
            '2': 'market',
            '202': 'market',
            '3': 'limit',
            '4': 'market',
            '5': 'limit',
            '6': 'market',
            '8': 'limit',
            '10': 'market',
        }
        return self.safe_string(statuses, status, status)

    async def watch_balance(self, params={}) -> Balances:
        """
        watch balance and get the amount of funds available for trading or funds locked in orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.type]: spot or contract if not provided self.options['defaultType'] is used
        :returns dict: a `balance structure <https://docs.ccxt.com/#/?id=balance-structure>`
        """
        await self.load_markets()
        type = None
        type, params = self.handle_market_type_and_params('watchBalance', None, params)
        messageHash = 'wallet:'
        method = None
        if type == 'spot':
            method = 'balanceSpot_subscribe'
            messageHash += 'spot'
        else:
            method = 'balanceMargin_subscribe'
            messageHash += 'margin'
        currencies = list(self.currencies.keys())
        return await self.watch_private(messageHash, method, currencies, params)

    def handle_balance(self, client: Client, message):
        #
        #   {
        #       "method":"balanceSpot_update",
        #       "params":[
        #          {
        #             "LTC":{
        #                "available":"0.16587",
        #                "freeze":"0"
        #             }
        #          }
        #       ],
        #       "id":null
        #   }
        #
        method = self.safe_string(message, 'method')
        data = self.safe_value(message, 'params')
        balanceDict = self.safe_value(data, 0)
        self.balance['info'] = balanceDict
        keys = list(balanceDict.keys())
        currencyId = self.safe_value(keys, 0)
        rawBalance = self.safe_value(balanceDict, currencyId)
        code = self.safe_currency_code(currencyId)
        account = self.account()
        account['free'] = self.safe_string(rawBalance, 'available')
        account['used'] = self.safe_string(rawBalance, 'freeze')
        self.balance[code] = account
        self.balance = self.safe_balance(self.balance)
        messageHash = 'wallet:'
        if method.find('Spot') >= 0:
            messageHash += 'spot'
        else:
            messageHash += 'margin'
        client.resolve(self.balance, messageHash)

    async def watch_public(self, messageHash, method, reqParams=[], params={}):
        url = self.urls['api']['ws']
        id = self.nonce()
        request = {
            'id': id,
            'method': method,
            'params': reqParams,
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def watch_multiple_subscription(self, messageHash, method, symbol, isNested=False, params={}):
        await self.load_markets()
        url = self.urls['api']['ws']
        id = self.nonce()
        client = self.safe_value(self.clients, url)
        request = None
        marketIds = []
        if client is None:
            subscription = {}
            market = self.market(symbol)
            marketId = market['id']
            subscription[marketId] = True
            marketIds = [marketId]
            if isNested:
                marketIds = [marketIds]
            request = {
                'id': id,
                'method': method,
                'params': marketIds,
            }
            message = self.extend(request, params)
            return await self.watch(url, messageHash, message, method, subscription)
        else:
            subscription = self.safe_value(client.subscriptions, method, {})
            hasSymbolSubscription = True
            market = self.market(symbol)
            marketId = market['id']
            isSubscribed = self.safe_value(subscription, marketId, False)
            if not isSubscribed:
                subscription[marketId] = True
                hasSymbolSubscription = False
            if hasSymbolSubscription:
                # already subscribed to self market(s)
                return await self.watch(url, messageHash, request, method, subscription)
            else:
                # resubscribe
                marketIdsNew = []
                marketIdsNew = list(subscription.keys())
                if isNested:
                    marketIdsNew = [marketIdsNew]
                resubRequest = {
                    'id': id,
                    'method': method,
                    'params': marketIdsNew,
                }
                if method in client.subscriptions:
                    del client.subscriptions[method]
                return await self.watch(url, messageHash, resubRequest, method, subscription)

    async def watch_private(self, messageHash, method, reqParams=[], params={}):
        self.check_required_credentials()
        await self.authenticate()
        url = self.urls['api']['ws']
        id = self.nonce()
        request = {
            'id': id,
            'method': method,
            'params': reqParams,
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def authenticate(self, params={}):
        self.check_required_credentials()
        url = self.urls['api']['ws']
        messageHash = 'authenticated'
        client = self.client(url)
        future = client.future('authenticated')
        authenticated = self.safe_value(client.subscriptions, messageHash)
        if authenticated is None:
            authToken = await self.v4PrivatePostProfileWebsocketToken()
            #
            #   {
            #       "websocket_token": "$2y$10$lxCvTXig/XrcTBFY1bdFseCKQmFTDtCpEzHNVnXowGplExFxPJp9y"
            #   }
            #
            token = self.safe_string(authToken, 'websocket_token')
            id = self.nonce()
            request = {
                'id': id,
                'method': 'authorize',
                'params': [
                    token,
                    'public',
                ],
            }
            subscription = {
                'id': id,
                'method': self.handle_authenticate,
            }
            try:
                await self.watch(url, messageHash, request, messageHash, subscription)
            except Exception as e:
                del client.subscriptions[messageHash]
                future.reject(e)
        return await future

    def handle_authenticate(self, client: Client, message):
        #
        #     {error: null, result: {status: "success"}, id: 1656084550}
        #
        future = client.futures['authenticated']
        future.resolve(1)
        return message

    def handle_error_message(self, client: Client, message):
        #
        #     {
        #         "error": {code: 1, message: "invalid argument"},
        #         "result": null,
        #         "id": 1656090882
        #     }
        #
        error = self.safe_value(message, 'error')
        try:
            if error is not None:
                code = self.safe_string(message, 'code')
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['ws']['exact'], code, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                client.reject(e, 'authenticated')
                if 'authenticated' in client.subscriptions:
                    del client.subscriptions['authenticated']
                return False
        return message

    def handle_message(self, client: Client, message):
        #
        # auth
        #    {error: null, result: {status: "success"}, id: 1656084550}
        #
        # pong
        #    {error: null, result: "pong", id: 0}
        #
        if not self.handle_error_message(client, message):
            return
        result = self.safe_value(message, 'result', {})
        if result is not None:
            if result == 'pong':
                self.handle_pong(client, message)
                return
        id = self.safe_integer(message, 'id')
        if id is not None:
            self.handle_subscription_status(client, message, id)
            return
        methods = {
            'market_update': self.handle_ticker,
            'trades_update': self.handle_trades,
            'depth_update': self.handle_order_book,
            'candles_update': self.handle_ohlcv,
            'ordersPending_update': self.handle_order,
            'ordersExecuted_update': self.handle_order,
            'balanceSpot_update': self.handle_balance,
            'balanceMargin_update': self.handle_balance,
            'deals_update': self.handle_my_trades,
        }
        topic = self.safe_value(message, 'method')
        method = self.safe_value(methods, topic)
        if method is not None:
            method(client, message)

    def handle_subscription_status(self, client: Client, message, id):
        # not every method stores its subscription
        # object so we can't do indeById here
        subs = client.subscriptions
        values = list(subs.values())
        for i in range(0, len(values)):
            subscription = values[i]
            if subscription is not True:
                subId = self.safe_integer(subscription, 'id')
                if (subId is not None) and (subId == id):
                    method = self.safe_value(subscription, 'method')
                    if method is not None:
                        method(client, message)
                        return

    def handle_pong(self, client: Client, message):
        client.lastPong = self.milliseconds()
        return message

    def ping(self, client):
        return {
            'id': 0,
            'method': 'ping',
            'params': [],
        }
