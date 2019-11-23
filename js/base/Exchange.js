"use strict";

const ccxt = require ('ccxt')
    , WebSocketClient = require ('./WebSocketClient')
    , {
        ExternallyResolvablePromise,
        externallyResolvablePromise
    } = require ('./MultiPromise')
    , {
        OrderBook,
        LimitedOrderBook,
        IndexedOrderBook,
        LimitedIndexedOrderBook,
    } = require ('./OrderBook')
    , log = require ('ololog').unlimited

module.exports = class Exchange extends ccxt.Exchange {

    orderbook (snapshot = {}) {
        return new OrderBook (snapshot)
    }

    limitedOrderBook (snapshot = {}, depth = undefined) {
        return new LimitedOrderBook (snapshot, depth)
    }

    indexedOrderBook (snapshot = {}) {
        return new IndexedOrderBook (snapshot)
    }

    limitedIndexedOrderBook (snapshot = {}, depth = undefined) {
        return new LimitedIndexedOrderBook (snapshot, depth)
    }

    websocket (url) {
        this.clients = this.clients || {}
        if (!this.clients[url]) {
            const callback = this.handleWsMessage.bind (this)
            this.clients[url] = new WebSocketClient (url, callback)
        }
        return this.clients[url]
    }

    sendWsMessage (url, messageHash, message = undefined, subscribeHash = undefined) {
        const client = this.websocket (url)
        if (!client.futures[messageHash]) {
            client.futures[messageHash] = externallyResolvablePromise ()
        }
        if (message && !client.subscriptions[subscribeHash]) {
            client.subscriptions[subscribeHash] = true
            message = this.signWsMessage (client, messageHash, message)
            client.send (message)
        }
        return client.futures[messageHash]
    }

    resolveWsFuture (client, messageHash, result) {
        if (client.futures[messageHash]) {
            const promise = client.futures[messageHash]
            promise.resolve (result)
            delete client.futures[messageHash]
        }
        return result
    }

    rejectWsFuture (client, messageHash, result) {
        if (client.futures[messageHash]) {
            const promise = client.futures[messageHash]
            promise.reject (result)
            delete client.futures[messageHash]
        }
        return result
    }

    async close () {
        const clients = Object.values (this.clients)
        for (let i = 0; i < clients.length; i++) {
            const client = clients[i]
            await client.close ()
        }
    }
}
