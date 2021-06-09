export class StakeData {
    private timestamp: Date;
    private stake: number;
  
    constructor(timestamp: Date, stake: number)
    {
        this.timestamp = timestamp;
        this.stake = stake;
    }

    getTimestamp(){
        return this.timestamp;
    }

    getStake(){
        return this.stake;
    }

}

export class StakeHistory {
    private stakeHistory: Array<StakeData>;

    constructor(){
        this.stakeHistory = new Array()
    }

    addStakeData(data: StakeData){
        this.stakeHistory.push(data)
    }

    monthlyData(){
        const monthlyData = new Map()
        this.stakeHistory.forEach((data: StakeData)=> {
            const month = data.getTimestamp().getMonth() + 1
            const year = data.getTimestamp().getFullYear()
            if (monthlyData.has(month +"/"+ year)){
                const amount = Number(monthlyData.get(month +"/"+ year)) + Number(data.getStake())
                monthlyData.set(month +"/"+year, amount)
            }
            else{
                monthlyData.set(month +"/"+year, data.getStake())
            }

        })
        return monthlyData
    }

    dailyData(){
        const dailyData = new Map()
        this.stakeHistory.forEach((data: StakeData)=> {
            const day = data.getTimestamp().getDate()
            const month = data.getTimestamp().getMonth() + 1
            const year = data.getTimestamp().getFullYear()
            if (dailyData.has(day+"/"+month +"/"+ year)){
                const amount = Number(dailyData.get(day+"/"+month +"/"+ year)) + Number(data.getStake())
                dailyData.set(day+"/"+month +"/"+ year, amount)
            }
            else{
                dailyData.set(day+"/"+month +"/"+ year, data.getStake())
            }

        })
        return dailyData
    }

    yearlyData(){
        const yearlyData = new Map()
        this.stakeHistory.forEach((data: StakeData)=> {
            const year = data.getTimestamp().getFullYear()
            if (yearlyData.has(year)){
                const amount = Number(yearlyData.get(year)) + Number(data.getStake())
                yearlyData.set(year, amount)
            }
            else{
                yearlyData.set(year, data.getStake())
            }

        })
        return yearlyData
    }
}