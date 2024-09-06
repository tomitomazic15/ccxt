import cryptocomRest from '../cryptocom.js';
import type { Int, OrderSide, OrderType, Str, Strings, OrderBook, Order, Trade, Ticker, OHLCV, Position, Balances, Num, Dict } from '../base/types.js';
import Client from '../base/ws/Client.js';
export default class cryptocom extends cryptocomRest {
    describe(): any;
    pong(client: any, message: any): Promise<void>;
    watchOrderBook(symbol: string, limit?: Int, params?: {}): Promise<OrderBook>;
    unWatchOrderBook(symbol: string, params?: {}): Promise<any>;
    watchOrderBookForSymbols(symbols: string[], limit?: Int, params?: {}): Promise<OrderBook>;
    unWatchOrderBookForSymbols(symbols: string[], params?: {}): Promise<OrderBook>;
    handleDelta(bookside: any, delta: any): void;
    handleDeltas(bookside: any, deltas: any): void;
    handleOrderBook(client: Client, message: any): void;
    watchTrades(symbol: string, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    unWatchTrades(symbol: string, params?: {}): Promise<Trade[]>;
    watchTradesForSymbols(symbols: string[], since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    unWatchTradesForSymbols(symbols: string[], params?: {}): Promise<any>;
    handleTrades(client: Client, message: any): void;
    watchMyTrades(symbol?: Str, since?: Int, limit?: Int, params?: {}): Promise<Trade[]>;
    watchTicker(symbol: string, params?: {}): Promise<Ticker>;
    unWatchTicker(symbol: string, params?: {}): Promise<any>;
    handleTicker(client: Client, message: any): void;
    watchOHLCV(symbol: string, timeframe?: string, since?: Int, limit?: Int, params?: {}): Promise<OHLCV[]>;
    unWatchOHLCV(symbol: string, timeframe?: string, params?: {}): Promise<any>;
    handleOHLCV(client: Client, message: any): void;
    watchOrders(symbol?: Str, since?: Int, limit?: Int, params?: {}): Promise<Order[]>;
    handleOrders(client: Client, message: any, subscription?: any): void;
    watchPositions(symbols?: Strings, since?: Int, limit?: Int, params?: {}): Promise<Position[]>;
    setPositionsCache(client: Client, type: any, symbols?: Strings): void;
    loadPositionsSnapshot(client: any, messageHash: any): Promise<void>;
    handlePositions(client: any, message: any): void;
    watchBalance(params?: {}): Promise<Balances>;
    handleBalance(client: Client, message: any): void;
    createOrderWs(symbol: string, type: OrderType, side: OrderSide, amount: number, price?: Num, params?: {}): Promise<Order>;
    handleOrder(client: Client, message: any): void;
    cancelOrderWs(id: string, symbol?: Str, params?: {}): Promise<Order>;
    cancelAllOrdersWs(symbol?: Str, params?: {}): Promise<any>;
    handleCancelAllOrders(client: Client, message: any): void;
    watchPublic(messageHash: any, params?: {}): Promise<any>;
    watchPublicMultiple(messageHashes: any, topics: any, params?: {}): Promise<any>;
    unWatchPublicMultiple(topic: string, symbols: string[], messageHashes: string[], subMessageHashes: string[], topics: string[], params?: {}, subExtend?: {}): Promise<any>;
    watchPrivateRequest(nonce: any, params?: {}): Promise<any>;
    watchPrivateSubscribe(messageHash: any, params?: {}): Promise<any>;
    handleErrorMessage(client: Client, message: any): boolean;
    handleSubscribe(client: Client, message: any): void;
    handleMessage(client: Client, message: any): void;
    authenticate(params?: {}): Promise<any>;
    handlePing(client: Client, message: any): void;
    handleAuthenticate(client: Client, message: any): void;
    handleUnsubscribe(client: Client, message: any): void;
    cleanCache(subscription: Dict): void;
}
