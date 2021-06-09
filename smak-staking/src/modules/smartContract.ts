import { TezosToolkit } from "@taquito/taquito";
import { StakeFlex } from "./stakeFlex"
import { StakeLock, StakeLockPack } from "./stakeLock"
import { StakeData, StakeHistory } from "./stakingHistory"

export class SmartContract{
    private address : string;
    private tk: TezosToolkit;

    constructor(address: string, tk: TezosToolkit){
      this.address = address;
      this.tk = tk;
    }

    async getStorage(){
        const t1 = performance.now()
        const contract = await this.tk.contract.at(this.address);
        const storage: any = await contract.storage();
        const t2 = performance.now()
        console.log("storage", t2-t1)
        return storage;
    }

    async getStakeFlex(storage: any, addr: string)
    {
        const t1 = performance.now()
        const sStakeFlex = await storage.userStakeFlexPack.get(addr)
        const t2 = performance.now()
        console.log("flex", t2-t1)
        return new StakeFlex(Number(sStakeFlex.reward), sStakeFlex.timestamp, Number(sStakeFlex.value))
    }

    async getLockStakeList(storage: any, addr: string)
    {
        const t0 = performance.now()
        const sAllStakeLock = await storage.userStakeLockPack.get(addr)
        const t1 = performance.now()
        const lockStakeList = new Map()

       
        sAllStakeLock.forEach((sLocks: object[], id: number) => {
            const pack = new StakeLockPack()
            sLocks.forEach((stake: any, index: number)=> {
                const stakeLock = new StakeLock(Number(stake.rate), stake.timestamp, Number(stake.value))
                pack.addStakeLockList(Number(index), stakeLock)
            })
            lockStakeList.set(Number(id), pack)
        });
        const t2 = performance.now()
        console.log("getting the right address", t1 -t0)
        console.log("computing the data", t2 - t1)
        return lockStakeList;
    }

    getStakeHistory(storage: any){
        const sHistory = storage.stakingHistory
        const stakeHistory = new StakeHistory()
        sHistory.forEach((data: number, timestamp: Date) => {
            const stakeData = new StakeData(new Date(timestamp), data)
            stakeHistory.addStakeData(stakeData)
        });
        console.log(stakeHistory.yearlyData())
        console.log(stakeHistory.monthlyData())
        console.log(stakeHistory.dailyData())
        console.log(stakeHistory)
        
    }

}
