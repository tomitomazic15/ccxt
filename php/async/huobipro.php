<?php

namespace ccxt\async;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception; // a common import

class huobipro extends huobi {

    public function describe() {
        // this is an alias for backward-compatibility
        // to be removed soon
        return $this->deep_extend(parent::describe(), array(
            'id' => 'huobipro',
            'alias' => true,
            'name' => 'Huobi Pro',
        ));
    }
}
