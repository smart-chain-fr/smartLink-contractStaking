export class StakeFlex {
    private reward: number;
    private timestamp: Date;
    private value: number;

    constructor(reward: number, timestamp : Date, value : number)
    {
        this.reward = reward;
        this.timestamp = timestamp;
        this.value = value;
    }

    getReward()
    {
        return this.reward;
    }

    getTimestamp()
    {
        return this.timestamp;
    }

    getValue(){
        return this.value;
    }
}

