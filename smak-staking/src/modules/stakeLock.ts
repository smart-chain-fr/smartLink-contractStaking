export class StakeLock {
    private rate: number;
    private timestamp: Date;
    private value: number;

    constructor(rate: number, timestamp : Date, value : number)
    {
        this.rate = rate;
        this.timestamp = timestamp;
        this.value = value;
    }

    getRate()
    {
        return this.rate;
    }

    getTimestamp()
    {
        return this.timestamp;
    }

    getValue(){
        return this.value;
    }
}

export class StakeLockPack {
    private stakeLockList: Map<number, StakeLock>;
   
    constructor()
    {
        this.stakeLockList = new Map()
    }

    getStakeLockList(){
        return this.stakeLockList;
    }

    addStakeLockList(index: number, stakeLock: StakeLock){
        this.stakeLockList.set(index, stakeLock)
    }
    
    getStakeLock(index:number){
        return this.stakeLockList.get(index);
    }
}