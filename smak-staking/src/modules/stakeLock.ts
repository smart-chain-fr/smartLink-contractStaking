export class StakeLock {
    public rate: number;
    public timestamp: Date;
    public value: number;

    constructor(rate: number, timestamp : Date, value : number)
    {
        this.rate = rate;
        this.timestamp = timestamp;
        this.value = value;
    }
}