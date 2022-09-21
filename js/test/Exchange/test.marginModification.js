'use strict';

const assert = require('assert');

function testMarginModification (exchange, marginModification) {

    const msgPrefix = exchange.id + ' ' + method + ' : ';

    const format = {
        info: {},
        type: 'add',
        amount: 0.1,
        total: 0.29934828,
        code: 'USDT',
        symbol: 'ADA/USDT:USDT',
        status: 'ok',
    };
    const keys = Object.keys(format);
    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        assert (key in marginModification, msgPrefix + key + ' is missing from structure');
    }
    assert (exchange.isObject (marginModification['info']));
    if (marginModification['type'] !== undefined) {
        assert ((marginModification['type'] === 'add') || (marginModification['type'] === 'reduce') || (marginModification['type'] === 'set'));
    }
    if (marginModification['amount'] !== undefined) {
        assert (typeof marginModification['amount'] === 'number');
    }
    if (marginModification['total'] !== undefined) {
        assert (typeof marginModification['total'] === 'number');
    }
    if (marginModification['code'] !== undefined) {
        assert (typeof marginModification['code'] === 'string');
    }
    if (marginModification['symbol'] !== undefined) {
        assert (typeof marginModification['symbol'] === 'string');
    }
    if (marginModification['status'] !== undefined) {
        assert (exchange.inArray (marginModification['status'], [ 'ok', 'pending', 'canceled', 'failed' ]));
    }
}

module.exports = testMarginModification;
