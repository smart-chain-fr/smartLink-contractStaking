// config.js
import dotenv from 'dotenv'
import path from 'path'

dotenv.config({
   path: path.resolve(__dirname, process.env.NODE_ENV + '.env')
});

export const config = {
    // Environment variables
    NODE_ENV: process.env.NODE_ENV,

    // Tezos Network variables
    RPC_ADDRESS: process.env.RPC_ADDRESS,   

    // Signer Variables
    ADDRESS: process.env.ADDRESS,
    SIGNER_EMAIL: process.env.SIGNER_EMAIL,
    SIGNER_PASSWORD: process.env.SIGNER_PASSWORD,
    SIGNER_MNEMONIC: process.env.SIGNER_MNEMONIC,
    SIGNER_SECRET: process.env.SIGNER_SECRET,

    // Contract Variables
    CONTRACT_FA12TOKEN_CONTRACT_ADDRESS: process.env.CONTRACT_FA12TOKEN_CONTRACT_ADDRESS,
    CONTRACT_RESERVE_ADDRESS: process.env.CONTRACT_RESERVE_ADDRESS
  }