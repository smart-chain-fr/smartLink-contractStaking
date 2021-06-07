var method = StakeFlex.prototype;

function StakeFlex(reward, timestamp, value)
{
    this._reward = reward;
    this._timestamp = timestamp;
    this._value = value;
}

method.getReward = function(){
    return this._reward;
};

method.getTimestamp = function(){
    return this._timestamp;
};

method.getValue = function(){
    return this._value;
};

mothod.getStakingFlex = function(){
    return {
        "reward": this._reward, 
        "timestamp": this._timestamp,
        "value": this._value
    }
}

module.exports = StakeFlex;