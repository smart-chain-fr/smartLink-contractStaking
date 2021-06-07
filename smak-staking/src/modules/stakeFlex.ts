export class StakeFlex {
    public reward: number;
    public timestamp: Date;
    public value: number;

    constructor(reward: number, timestamp : Date, value : number)
    {
        this.reward = reward;
        this.timestamp = timestamp;
        this.value = value;
    }
}

