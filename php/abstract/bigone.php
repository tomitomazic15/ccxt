<?php

namespace ccxt\abstract;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code


abstract class bigone extends \ccxt\Exchange {
    public function public_get_ping($params = array()) {
        return $this->request('ping', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs($params = array()) {
        return $this->request('asset_pairs', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs_asset_pair_name_depth($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/depth', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs_asset_pair_name_trades($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/trades', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs_asset_pair_name_ticker($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/ticker', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs_asset_pair_name_candles($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/candles', 'public', 'GET', $params, null, null, array());
    }
    public function public_get_asset_pairs_tickers($params = array()) {
        return $this->request('asset_pairs/tickers', 'public', 'GET', $params, null, null, array());
    }
    public function private_get_accounts($params = array()) {
        return $this->request('accounts', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_fund_accounts($params = array()) {
        return $this->request('fund/accounts', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_assets_asset_symbol_address($params = array()) {
        return $this->request('assets/{asset_symbol}/address', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_orders($params = array()) {
        return $this->request('orders', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_orders_id($params = array()) {
        return $this->request('orders/{id}', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_orders_multi($params = array()) {
        return $this->request('orders/multi', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_trades($params = array()) {
        return $this->request('trades', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_withdrawals($params = array()) {
        return $this->request('withdrawals', 'private', 'GET', $params, null, null, array());
    }
    public function private_get_deposits($params = array()) {
        return $this->request('deposits', 'private', 'GET', $params, null, null, array());
    }
    public function private_post_orders($params = array()) {
        return $this->request('orders', 'private', 'POST', $params, null, null, array());
    }
    public function private_post_orders_id_cancel($params = array()) {
        return $this->request('orders/{id}/cancel', 'private', 'POST', $params, null, null, array());
    }
    public function private_post_orders_cancel($params = array()) {
        return $this->request('orders/cancel', 'private', 'POST', $params, null, null, array());
    }
    public function private_post_withdrawals($params = array()) {
        return $this->request('withdrawals', 'private', 'POST', $params, null, null, array());
    }
    public function private_post_transfer($params = array()) {
        return $this->request('transfer', 'private', 'POST', $params, null, null, array());
    }
    public function contractpublic_get_symbols($params = array()) {
        return $this->request('symbols', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractpublic_get_instruments($params = array()) {
        return $this->request('instruments', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractpublic_get_depth_symbol_snapshot($params = array()) {
        return $this->request('depth@{symbol}/snapshot', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractpublic_get_instruments_difference($params = array()) {
        return $this->request('instruments/difference', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractpublic_get_instruments_prices($params = array()) {
        return $this->request('instruments/prices', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_accounts($params = array()) {
        return $this->request('accounts', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_orders_id($params = array()) {
        return $this->request('orders/{id}', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_orders($params = array()) {
        return $this->request('orders', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_orders_opening($params = array()) {
        return $this->request('orders/opening', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_orders_count($params = array()) {
        return $this->request('orders/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_orders_opening_count($params = array()) {
        return $this->request('orders/opening/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_trades($params = array()) {
        return $this->request('trades', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_get_trades_count($params = array()) {
        return $this->request('trades/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractprivate_post_orders($params = array()) {
        return $this->request('orders', 'contractPrivate', 'POST', $params, null, null, array());
    }
    public function contractprivate_post_orders_batch($params = array()) {
        return $this->request('orders/batch', 'contractPrivate', 'POST', $params, null, null, array());
    }
    public function contractprivate_put_positions_symbol_margin($params = array()) {
        return $this->request('positions/{symbol}/margin', 'contractPrivate', 'PUT', $params, null, null, array());
    }
    public function contractprivate_put_positions_symbol_risk_limit($params = array()) {
        return $this->request('positions/{symbol}/risk-limit', 'contractPrivate', 'PUT', $params, null, null, array());
    }
    public function contractprivate_delete_orders_id($params = array()) {
        return $this->request('orders/{id}', 'contractPrivate', 'DELETE', $params, null, null, array());
    }
    public function contractprivate_delete_orders_batch($params = array()) {
        return $this->request('orders/batch', 'contractPrivate', 'DELETE', $params, null, null, array());
    }
    public function webexchange_get_v3_assets($params = array()) {
        return $this->request('v3/assets', 'webExchange', 'GET', $params, null, null, array());
    }
    public function publicGetPing($params = array()) {
        return $this->request('ping', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairs($params = array()) {
        return $this->request('asset_pairs', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairsAssetPairNameDepth($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/depth', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairsAssetPairNameTrades($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/trades', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairsAssetPairNameTicker($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/ticker', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairsAssetPairNameCandles($params = array()) {
        return $this->request('asset_pairs/{asset_pair_name}/candles', 'public', 'GET', $params, null, null, array());
    }
    public function publicGetAssetPairsTickers($params = array()) {
        return $this->request('asset_pairs/tickers', 'public', 'GET', $params, null, null, array());
    }
    public function privateGetAccounts($params = array()) {
        return $this->request('accounts', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetFundAccounts($params = array()) {
        return $this->request('fund/accounts', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetAssetsAssetSymbolAddress($params = array()) {
        return $this->request('assets/{asset_symbol}/address', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetOrders($params = array()) {
        return $this->request('orders', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetOrdersId($params = array()) {
        return $this->request('orders/{id}', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetOrdersMulti($params = array()) {
        return $this->request('orders/multi', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetTrades($params = array()) {
        return $this->request('trades', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetWithdrawals($params = array()) {
        return $this->request('withdrawals', 'private', 'GET', $params, null, null, array());
    }
    public function privateGetDeposits($params = array()) {
        return $this->request('deposits', 'private', 'GET', $params, null, null, array());
    }
    public function privatePostOrders($params = array()) {
        return $this->request('orders', 'private', 'POST', $params, null, null, array());
    }
    public function privatePostOrdersIdCancel($params = array()) {
        return $this->request('orders/{id}/cancel', 'private', 'POST', $params, null, null, array());
    }
    public function privatePostOrdersCancel($params = array()) {
        return $this->request('orders/cancel', 'private', 'POST', $params, null, null, array());
    }
    public function privatePostWithdrawals($params = array()) {
        return $this->request('withdrawals', 'private', 'POST', $params, null, null, array());
    }
    public function privatePostTransfer($params = array()) {
        return $this->request('transfer', 'private', 'POST', $params, null, null, array());
    }
    public function contractPublicGetSymbols($params = array()) {
        return $this->request('symbols', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractPublicGetInstruments($params = array()) {
        return $this->request('instruments', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractPublicGetDepthSymbolSnapshot($params = array()) {
        return $this->request('depth@{symbol}/snapshot', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractPublicGetInstrumentsDifference($params = array()) {
        return $this->request('instruments/difference', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractPublicGetInstrumentsPrices($params = array()) {
        return $this->request('instruments/prices', 'contractPublic', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetAccounts($params = array()) {
        return $this->request('accounts', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetOrdersId($params = array()) {
        return $this->request('orders/{id}', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetOrders($params = array()) {
        return $this->request('orders', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetOrdersOpening($params = array()) {
        return $this->request('orders/opening', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetOrdersCount($params = array()) {
        return $this->request('orders/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetOrdersOpeningCount($params = array()) {
        return $this->request('orders/opening/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetTrades($params = array()) {
        return $this->request('trades', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivateGetTradesCount($params = array()) {
        return $this->request('trades/count', 'contractPrivate', 'GET', $params, null, null, array());
    }
    public function contractPrivatePostOrders($params = array()) {
        return $this->request('orders', 'contractPrivate', 'POST', $params, null, null, array());
    }
    public function contractPrivatePostOrdersBatch($params = array()) {
        return $this->request('orders/batch', 'contractPrivate', 'POST', $params, null, null, array());
    }
    public function contractPrivatePutPositionsSymbolMargin($params = array()) {
        return $this->request('positions/{symbol}/margin', 'contractPrivate', 'PUT', $params, null, null, array());
    }
    public function contractPrivatePutPositionsSymbolRiskLimit($params = array()) {
        return $this->request('positions/{symbol}/risk-limit', 'contractPrivate', 'PUT', $params, null, null, array());
    }
    public function contractPrivateDeleteOrdersId($params = array()) {
        return $this->request('orders/{id}', 'contractPrivate', 'DELETE', $params, null, null, array());
    }
    public function contractPrivateDeleteOrdersBatch($params = array()) {
        return $this->request('orders/batch', 'contractPrivate', 'DELETE', $params, null, null, array());
    }
    public function webExchangeGetV3Assets($params = array()) {
        return $this->request('v3/assets', 'webExchange', 'GET', $params, null, null, array());
    }
}
