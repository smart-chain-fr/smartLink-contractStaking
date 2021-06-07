var method = StakeLockPacksList.prototype;

function StakeLockPacksList()
{
    this._stakeLockPacksList = new Map();
}

method.getStakeLockPacksList = function(){
    return this._stakeLockPacksList;
};

method.getStakeLock = function(pack_id, stake_id){
    return this._stakeLockPacksList.get(pack_id).getStakeLock(stake_id)
};

method.addStakeLockPack = function(id, pack){
    this._stakeLockPacksList.set(id, pack)
}

module.exports = StakeLockPacksList;