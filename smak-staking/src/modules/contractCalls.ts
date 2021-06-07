import { TezosToolkit } from "@taquito/taquito";
import { config } from "../../config/config";
import { NetworkType } from "@airgap/beacon-sdk";
import { BeaconWallet } from "@taquito/beacon-wallet";

export class ContractCalls{
    private tk: TezosToolkit;
    private wallet: BeaconWallet;
    private network: NetworkType;

    constructor(){
        // Set the RPC
        this.tk = new TezosToolkit(config.RPC_ADDRESS);
        
        // Set the network
        this.network = (config.NODE_ENV=="development")?NetworkType.EDONET:NetworkType.MAINNET;
        
        // Set the wallet
        const options = {
            name: 'SMAK Staking',
            iconUrl: 'https://tezostaquito.io/img/favicon.png',
            preferredNetwork: this.network,
            eventHandlers: {
              PERMISSION_REQUEST_SUCCESS: {
                handler: async (data: any) => {
                  console.log('permission data:', data);
                },
              },
            },
        };
        this.wallet = new BeaconWallet(options);
    }

    public async setupWallet(){
        // Request the permission
        await this.wallet.requestPermissions({
            network: {
              type: this.network,
            },
          });

        // Set the wallet provider for later
        this.tk.setWalletProvider(this.wallet);
        
        const address = await this.wallet.getPKH();
        return address;
    }
}
