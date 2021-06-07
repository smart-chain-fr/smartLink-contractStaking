const config = require('../config/config.js');


module.exports = 
{
    "prim": "Pair",
    "args": [
        {
            "prim": "Pair",
            "args": [
                {
                    "prim": "Pair",
                    "args": [
                        {
                            "string": config.CONTRACT_FA12TOKEN_CONTRACT_ADDRESS
                        },
                        {
                            "string": config.ADDRESS
                        }
                    ]
                },
                {
                    "prim": "Pair",
                    "args": [
                        [],
                        {
                            "string": config.CONTRACT_RESERVE_ADDRESS
                        }
                    ]
                }
            ]
        },
        {
            "prim": "Pair",
            "args": [
                {
                    "prim": "Pair",
                    "args": [
                        [],
                        []
                    ]
                },
                {
                    "prim": "Pair",
                    "args": [
                        [],
                        {
                            "prim": "Pair",
                            "args": [
                                [],
                                {
                                    "prim": "None"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}