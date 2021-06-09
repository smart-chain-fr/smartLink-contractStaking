export class StakeOption {
    private minStake: number;
    private maxStake: number;
    private stakingPeriod: number;
    private stakingPerecentage: number;
   
    constructor(minStake: number, maxStake: number, stakingPeriod: number, stakingPercentage: number)
    {
        this.minStake = minStake;
        this.maxStake = maxStake;
        this.stakingPeriod = stakingPeriod;
        this.stakingPerecentage = stakingPercentage;
    }

  
    getMaxStake(){
        return this.maxStake;
    }

    getMinStake(){
        return this.minStake;
    }

    getStakingPeriod(){
        return this.stakingPeriod;
    }

    getStakingPercentage(){
        return this.stakingPerecentage;
    }

}