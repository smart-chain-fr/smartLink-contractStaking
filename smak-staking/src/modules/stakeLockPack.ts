import { StakeLock } from './stakeLock'

export class StakeLockPack {
    public id: number;
    public stakeLockList: Map<number, StakeLock>;
   
    constructor(id: number)
    {
        this.id = id;
        this.stakeLockList = new Map()
    }
}