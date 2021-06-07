import { Component, Vue } from 'vue-property-decorator';
import { ContractCalls } from '../../modules/contractCalls'
@Component
export default class Staking extends Vue {
    private wallet: ContractCalls = new ContractCalls();

    async connection(){
        const addr = await this.wallet.setupWallet();
        console.log(addr)
    }

}