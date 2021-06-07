import { Component, Vue } from 'vue-property-decorator';
import { Wallet } from '../../modules/wallet'
@Component
export default class Staking extends Vue {
    private wallet: Wallet = new Wallet();

    async connection(){
        const addr = await this.wallet.setupWallet();
        console.log(addr)
    }

}