// config.js
const dotenv = require('dotenv');
const path = require('path');

dotenv.config({
   path: path.resolve(__dirname, process.env.NODE_ENV + '.env')
});

module.exports = {
    // Environment variables
    NODE_ENV: process.env.NODE_ENV,

    // Tezos Network variables
    RPC_ADDRESS: process.env.RPC_ADDRESS,   

    // Signer Variables
    SIGNER_EMAIL: process.env.SIGNER_EMAIL,
    SIGNER_PASSWORD: process.env.SIGNER_PASSWORD,
    SIGNER_MNEMONIC: process.env.SIGNER_MNEMONIC,
    SIGNER_SECRET: process.env.SIGNER_SECRET
  }