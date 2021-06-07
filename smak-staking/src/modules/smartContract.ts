import { TezosToolkit } from "@taquito/taquito";
import { config } from "../../config/config";

export class SmartContract{
    private address : string;
    private tk: TezosToolkit;

    constructor(address: string){
      this.address = address;
      this.tk = new TezosToolkit(config.RPC_ADDRESS);
    }

    async getStorage(){
        const contract = await this.tk.contract.at(this.address);
        const storage: any = await contract.storage();
        return storage;
    }
}
