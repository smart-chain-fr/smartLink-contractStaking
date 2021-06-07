var method = StakeLockPack.prototype;

function StakeLockPack(id)
{
    this._id = id;
    this._stakeLockList = new Map();
}

method.getId = function(){
    return this._id;
};

method.getStakeLockList = function(){
    return this._stakeLockList;
};

method.getStakeLock = function(id){
    return this._stakeLockList.get(id);
};

method.getValue = function(){
    return this._value;
};

method.getStakingLock = function(){
    return {
        "id": this._id,
        "stakeLockList": this._stakeLockList
    }
}

method.addStakeLock = function(id, stakeLock){
    this._stakeLockList.set(id, stakeLock)
}

module.exports = StakeLockPack;