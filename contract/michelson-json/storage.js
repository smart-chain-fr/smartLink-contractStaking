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
                        [
                            {
                                "prim": "Elt",
                                "args": [
                                    {
                                        "string": "authors"
                                    },
                                    {
                                        "bytes": "536d6172746c696e6b20446576205465616d203c656d61696c40646f6d61696e2e636f6d3e"
                                    }
                                ]
                            },
                            {
                                "prim": "Elt",
                                "args": [
                                    {
                                        "string": "description"
                                    },
                                    {
                                        "bytes": "534d414b205374616b696e6720736d6172742d636f6e7472616374"
                                    }
                                ]
                            },
                            {
                                "prim": "Elt",
                                "args": [
                                    {
                                        "string": "homepage"
                                    },
                                    {
                                        "bytes": "68747470733a2f2f736d61727470792e696f"
                                    }
                                ]
                            },
                            {
                                "prim": "Elt",
                                "args": [
                                    {
                                        "string": "interfaces"
                                    },
                                    {
                                        "bytes": "545a49502d3031362d323032312d30342d3137"
                                    }
                                ]
                            },
                            {
                                "prim": "Elt",
                                "args": [
                                    {
                                        "string": "name"
                                    },
                                    {
                                        "bytes": "534d414b205374616b696e67"
                                    }
                                ]
                            }
                        ],
                        {
                            "prim": "Pair",
                            "args": [
                                {
                                    "int": "0"
                                },
                                {
                                    "int": "0"
                                }
                            ]
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
                        {
                            "string": config.CONTRACT_RESERVE_ADDRESS
                        },
                        {
                            "prim": "Pair",
                            "args": [
                                [
                                    {
                                        "prim": "Elt",
                                        "args": [
                                            {
                                                "string": new Date(Date.now()).toISOString()
                                            },
                                            {
                                                "int": "0"
                                            }
                                        ]
                                    }
                                ],
                                [
                                    {
                                        "prim": "Elt",
                                        "args": [
                                            {
                                                "int": "0"
                                            },
                                            {
                                                "prim": "Pair",
                                                "args": [
                                                    {
                                                        "prim": "Pair",
                                                        "args": [
                                                            {
                                                                "int": config.FLEX_MAX
                                                            },
                                                            {
                                                                "int": "0"
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "prim": "Pair",
                                                        "args": [
                                                            {
                                                                "int": config.FLEX_PERCENTAGE
                                                            },
                                                            {
                                                                "int": "0"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            ]
                        }
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
