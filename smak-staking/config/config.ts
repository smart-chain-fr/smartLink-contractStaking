// config.js
import dotenv from 'dotenv'
import path from 'path'

dotenv.config({
   path: path.resolve(__dirname, process.env.NODE_ENV + '.env')
});

export const config = {
    // Environment variables
    NODE_ENV: process.env.NODE_ENV || 'development',

    // Tezos Network variables
    RPC_ADDRESS: process.env.RPC_ADDRESS || 'https://edonet.smartpy.io',  
    
    SMART_CONTRACT_ADDRESS: process.env.SMART_CONTRACT_ADDRESS ||'KT1FQDLKzpnD6FNMkCVTTTmSwF27mZCXQ9ns'

}