import { Component, Vue } from 'vue-property-decorator';
import { Wallet } from '../../modules/wallet'
import { SmartContract } from '../../modules/smartContract'
import { config } from '../../../config/config'
import { TezosToolkit } from '@taquito/taquito';

const tk = new TezosToolkit(config.RPC_ADDRESS);
@Component
export default class Staking extends Vue {
    private wallet: Wallet = new Wallet(tk);
    private smartContract: SmartContract = new SmartContract(config.SMART_CONTRACT_ADDRESS, tk)
    private storage: any;

    async connection(){
        this.storage = await this.smartContract.getStorage()
        const addr = await this.wallet.setupWallet();
        console.log(addr)
        const flex = await this.smartContract.getStakeFlex(this.storage, addr)
        console.log(flex)
        const lock = await this.smartContract.getLockStakeList(this.storage, addr)
        console.log(lock)
        const history = await this.smartContract.getStakeHistory(this.storage)
    }




}