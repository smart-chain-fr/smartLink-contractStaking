/**
 * @module smart-link-ICO
 * @author Smart-Chain
 * @version 1.0.0
 * This module originates a FA 1.2 token smart contract with a freeze function
 */

 var signer = require("@taquito/signer"); // Used to initialize a signer
 
 var taquito = require("@taquito/taquito"); // Used for the taquito calls to the smart contract
 const config = require('../config/config.js'); // Config file with config variables
 var storage = require('../michelson-json/storage.js') // Initial storage of the smart contract
 // Connection to the Tezos RPC
 var Tezos = new taquito.TezosToolkit(config.RPC_ADDRESS);
 
 /**
 * Function that originates a smart contract with the signer key
 */
 async function originate() {
    
     if (config.NODE_ENV == "development"){
         // Import the signer account
         signer.importKey(
             Tezos,
             config.SIGNER_EMAIL,
             config.SIGNER_PASSWORD,
             config.SIGNER_MNEMONIC,
             config.SIGNER_SECRET
         );
 
     }
     else {
         //import signer
         const s = await signer.InMemorySigner.fromSecretKey(config.SIGNER_SECRET, config.SIGNER_MNEMONIC)
         Tezos.setProvider({ signer: s });
     }
 
     // Originate the contract
     const originationOp = await Tezos.contract.originate({
         // Smart contract Michelson JSON code
         code: require('./ICO-contract.json'),
         init: storage
     }).catch(error => {
         console.log(error)
     });
 
     console.log("SmartLink API: Waiting for confirmation of origination for " + originationOp.contractAddress + "...");
 
     // Waiting for the origination to be completed/confirmed 
     await originationOp.confirmation()
         .catch(error => {
             console.log(error)
         });
 
     console.log("SmartLink API: Origination completed.");
 
 }
 
 originate();