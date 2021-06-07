var method = StakeLock.prototype;

function StakeLock(rate, timestamp, value)
{
    this._rate = rate;
    this._timestamp = timestamp;
    this._value = value;
}

method.getRate = function(){
    return this._rate;
};

method.getTimestamp = function(){
    return this._timestamp;
};

method.getValue = function(){
    return this._value;
};

mothod.getStakingLock = function(){
    return {
        "rate": this._rate,
        "timestamp": this._timestamp,
        "value": this._value
    }
}

module.exports = StakeLock;