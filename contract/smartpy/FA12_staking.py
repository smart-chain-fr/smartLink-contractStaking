import smartpy as sp
class Error:
    def make(s): return (s)

    NotAdmin                        = make("Access denied")
    AmountTooHigh                   = make("Amount is too high")
    AmountTooLow                    = make("Amount is too low")
    DupStakingOpt                   = make("A staking option with this Id already exists")
    NotStakingOpt                   = make("The staking option for this id does not exist")
    NeverStaked                     = make("Never staked on this contract")
    NeverUsedPack                   = make("Never staked using this pack")
    NotStaking                      = make("This stake doesn't exist")
    BalanceTooLow                   = make("Not enough tokens to unstake")
    StakingFlexRate                 = make("Can't update the staking flex rate with this function")


StakeLock = sp.TRecord(
    timestamp=sp.TTimestamp,
    period = sp.TInt,
    rate=sp.TNat,
    value=sp.TNat
)

StakeFlex = sp.TRecord(
    timestamp=sp.TTimestamp,
    value=sp.TNat,
    reward=sp.TNat
)

UserStakeFlexPack = sp.big_map(tkey=sp.TAddress, tvalue = StakeFlex)

UserStakeLockPack = sp.big_map(
    tkey=sp.TAddress,
    tvalue=sp.TMap(
        sp.TNat,
        sp.TMap(
            sp.TNat,
            StakeLock)
    )
)

TotalReward = sp.big_map(tkey = sp.TAddress, tvalue = sp.TNat)

Options = sp.map(
    l = {sp.nat(0):sp.record(minStake = 0, maxStake = 1000000, stakingPeriod = 0, stakingPercentage = 20)},
    tkey=sp.TNat,
    tvalue= sp.TRecord(
            minStake=sp.TNat,
            maxStake=sp.TNat,
            stakingPeriod=sp.TInt,
            stakingPercentage=sp.TNat
        )
    )

def call(c, x):
    sp.transfer(x, sp.mutez(0), c)

class FA12Staking_core(sp.Contract):
    def __init__(self, contract, admin, reserve, metadata_url, **kargs):
        self.init(
            FA12TokenContract=contract,
            admin=admin,
            reserve=reserve,
            userStakeLockPack=UserStakeLockPack,
            userStakeFlexPack=UserStakeFlexPack,
            stakingOptions=Options,
            votingContract = sp.none,
            stakingHistory = sp.map(l={sp.timestamp(0):0},tkey = sp.TTimestamp, tvalue = sp.TInt),
            numberOfStakers=sp.int(0),
            redeemedRewards = sp.map(tkey = sp.TAddress, tvalue = sp.TNat),
            metadata = sp.big_map({"":metadata_url}),
            **kargs
        )

    @sp.entry_point
    def updateMetadata(self,params):
            sp.set_type(params, sp.TRecord(url = sp.TBytes))
            self.data.metadata[""] = params.url

    # The function updateReserve will update the reserve address
    # The function takes as parameter:
    # - the new reserve address
    @sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.reserve = params.reserve

    # The function updateAdmin will update the admin address
    # The function takes as parameter:
    # - the new admin address
    @sp.entry_point
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.admin = params.admin
    
    # The function updateContract will update the address of the token contract
    # The function takes as parameter:
    # - the new token contract address
    @sp.entry_point
    def updateContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.FA12TokenContract = params.contract
    
    
    # The function updateVotingContract will update the address of the voting contract
    # The function takes as parameter:
    # - the new voting contract address
    @sp.entry_point
    def updateVotingContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.votingContract = sp.some(params.contract)
    

    @sp.sub_entry_point
    def is_voting_contract(self, contract):
        sp.if self.data.votingContract.is_some():
            sp.result(self.data.votingContract.open_some() == contract)
        sp.else:
            sp.result(False)

    # The createStakingOption function is used to create a staking pack (period/APY). Only the admin can call this function
    # The function takes as parameters:
    # - the id of the staking parameters
    # - the staking rate
    # - the maximum staking amount per transaction
    # - the minimum staking amount per transaction
    # - the staking period
    @sp.entry_point
    def createStakingOption(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat, _max = sp.TNat, _min = sp.TNat, duration = sp.TInt).layout(("_id as id", ("rate", ("_max as max", ("_min as min", "duration"))))))
        sp.verify(~self.data.stakingOptions.contains(params._id), Error.DupStakingOpt)
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        option = sp.record(
            minStake = params._min,
            maxStake = params._max,
            stakingPeriod = params.duration,
            stakingPercentage = params.rate
        )
        self.data.stakingOptions[params._id] = option
    
    
    # The function updateStakingOptionRate will update the rate of a specified staking pack
    # The function takes as parameters:
    # - the staking pack id
    # - the staking pack new rate
    @sp.entry_point
    def updateStakingOptionRate(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat).layout(("_id as id", "rate")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].stakingPercentage = params.rate


    # The function updateStakingOptionDuration will update the duration of the staking pack
    # The function takes as parameters:
    # - the staking pack id
    # - the staking pack new duration
    @sp.entry_point
    def updateStakingOptionDuration(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, duration = sp.TInt).layout(("_id as id", "duration")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].stakingPeriod = params.duration
    

    # The function updateStakingOptionMax will update the max a user can stake in one transaction
    # The function takes as parameters:
    # - the staking pack id
    # - the staking pack new max amount per transaction 
    @sp.entry_point
    def updateStakingOptionMax(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _max = sp.TNat).layout(("_id as id", "_max as max")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].maxStake = params._max
    
    # The function updateStakingOptionMax will update the min a user can stake in one transaction
    # The function takes as parameters:
    # - the staking pack id
    # - the staking pack new min amount per transaction 
    @sp.entry_point
    def updateStakingOptionMin(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _min = sp.TNat).layout(("_id as id", "_min as min")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].minStake = params._min
  

class FA12Staking_methods(FA12Staking_core):
    
    def addStaker(self, addr):
        sp.if (~self.data.userStakeLockPack.contains(addr) & ~self.data.userStakeFlexPack.contains(addr)):
            self.data.numberOfStakers = self.data.numberOfStakers + 1
        
    def delStaker(self, addr):
        sp.if (~self.data.userStakeLockPack.contains(addr) & ~self.data.userStakeFlexPack.contains(addr)):
            self.data.numberOfStakers = self.data.numberOfStakers - 1
      
    def updateRedeemedRewards(self, addr, value):
        sp.if self.data.redeemedRewards.contains(addr):
            self.data.redeemedRewards[addr] = self.data.redeemedRewards[addr] + value
        sp.else:
            self.data.redeemedRewards[addr] = value
            
    @sp.entry_point
    def purgeStakingHistory(self, params):
        sp.set_type(params, sp.TRecord(timestamp_list = sp.TList(sp.TTimestamp)))
        sp.verify(sp.sender == self.data.admin, Error.NotAdmin)
        sp.for i in params.timestamp_list:
            del self.data.stakingHistory[i]
        

    # The updateStakingFlex function will add the amount to the stake and update the timestamp
    # The function takes as parameters:
    # - the address of the sender
    # - the amount the user wants to add to the staking
    def updateStakingFlex(self, addr, amount):
        self.data.userStakeFlexPack[addr].reward += self.getReward(sp.record(start = self.data.userStakeFlexPack[addr].timestamp, end = sp.now.add_seconds(0),  value = self.data.userStakeFlexPack[addr].value, rate = self.data.stakingOptions[0].stakingPercentage))
        self.data.userStakeFlexPack[addr].value += amount
        self.data.userStakeFlexPack[addr].timestamp = sp.now.add_seconds(0)

    # The stakeLock function will create a staking lock with the parameters of the specified pack
    # The function takes as parameters:
    # - the pack id
    # - the staking index
    @sp.entry_point
    def stakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, amount = sp.TNat))
        
        sp.verify(params.amount > self.data.stakingOptions[params.pack].minStake, Error.AmountTooLow)
        sp.verify(params.amount < self.data.stakingOptions[params.pack].maxStake, Error.AmountTooHigh)
        sp.verify(self.data.stakingOptions.contains(params.pack), Error.NotStakingOpt)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=sp.sender, to_=self.data.reserve, value=params.amount)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        
        staking = sp.record(timestamp=sp.now.add_seconds(0), rate = self.data.stakingOptions[params.pack].stakingPercentage, period = self.data.stakingOptions[params.pack].stakingPeriod,value = params.amount)
        
        self.addStaker(sp.sender)
        sp.if ~self.data.userStakeLockPack.contains(sp.sender):
            self.data.userStakeLockPack[sp.sender] = sp.map({params.pack :sp.map(l= {sp.nat(0):staking})})
        sp.else:
            sp.if ~self.data.userStakeLockPack[sp.sender].contains(params.pack):
                self.data.userStakeLockPack[sp.sender][params.pack] = sp.map({sp.nat(0):staking})
            sp.else:
                index = sp.len(self.data.userStakeLockPack[sp.sender][params.pack])
                self.data.userStakeLockPack[sp.sender][params.pack][index] = staking
        #clés
        self.data.stakingHistory[sp.now.add_seconds(0)] = sp.to_int(params.amount)
        

    # The stakeFlex function will create a staking flex with the parameters of the current staking flex parameters
    # The function takes as parameter:
    # - The amount staked
    @sp.entry_point
    def stakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
        
        sp.verify(params.amount > self.data.stakingOptions[0].minStake, Error.AmountTooLow)
        sp.verify(params.amount < self.data.stakingOptions[0].maxStake, Error.AmountTooHigh)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=sp.sender, to_=self.data.reserve, value=params.amount)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        self.addStaker(sp.sender)
        sp.if ~self.data.userStakeFlexPack.contains(sp.sender):
            self.data.userStakeFlexPack[sp.sender] = sp.record(timestamp = sp.now.add_seconds(0), value = params.amount + sp.nat(0), reward = sp.nat(0))
        sp.else:
            self.updateStakingFlex(sp.sender, params.amount)
            
        self.data.stakingHistory[sp.now.add_seconds(0)] = sp.to_int(params.amount)

    # The unstakeLock function will unstake a locked staking
    # The function takes as parameters:
    # - the staking pack
    # - the index of the staking
    @sp.entry_point
    def unstakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack=sp.TNat, index=sp.TNat))
        
        sp.verify(self.data.stakingOptions.contains(params.pack), Error.NotStakingOpt)
        sp.verify(self.data.userStakeLockPack.contains(sp.sender), Error.NeverStaked)
        sp.verify(self.data.userStakeLockPack[sp.sender].contains(params.pack), Error.NeverUsedPack)
        sp.verify(self.data.userStakeLockPack[sp.sender][params.pack].contains(params.index), Error.NotStaking)

        sp.if self.data.userStakeLockPack[sp.sender][params.pack][params.index].timestamp.add_seconds(self.data.userStakeLockPack[sp.sender][params.pack][params.index].period) < sp.now:
            self.unlockWithReward(params)
        sp.else:
            self.unlockWithoutReward(params)
            
        self.delStaker(sp.sender)
        
            
    # The unlockWithReward function will send the tokens back to the user with the rewards
    # The function takes as parameters:
    # - the staking pack
    # - the index of the staking
    @sp.sub_entry_point
    def unlockWithReward(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, index = sp.TNat))
        staking = self.data.userStakeLockPack[sp.sender][params.pack][params.index]
        amount = staking.value 
        reward = self.getReward(sp.record(start = staking.timestamp, end = staking.timestamp.add_seconds(staking.period), value = staking.value, rate = staking.rate))
        amount += reward
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract,entry_point="transfer").open_some(), paramCall)
        self.updateRedeemedRewards(sp.sender, reward)
        self.data.stakingHistory[sp.now.add_seconds(0)] = -1 * sp.to_int(amount)
        del self.data.userStakeLockPack[sp.sender][params.pack][params.index]
        
    
    # The unlockWithoutReward function will send the tokens back to the user without the reward
    # The function takes as parameters:
    # - the staking pack
    # - the index of the staking
    @sp.sub_entry_point
    def unlockWithoutReward(self, params):
        sp.set_type(params, sp.TRecord(index = sp.TNat, pack = sp.TNat))
        amount = self.data.userStakeLockPack[sp.sender][params.pack][params.index].value
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract,entry_point="transfer").open_some(), paramCall)
        self.data.stakingHistory[sp.now.add_seconds(0)] = -1 * sp.to_int(amount)
        del self.data.userStakeLockPack[sp.sender][params.pack][params.index]
        
    
    # The function unstakeFlex will send the specified amount of tokens to the user
    # The function takes as parameter
    # - the amount to unstake
    @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
        
        sp.verify(self.data.userStakeFlexPack.contains(sp.sender), Error.NeverStaked)
        sp.verify(self.data.userStakeFlexPack[sp.sender].value >= params.amount, Error.BalanceTooLow)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=params.amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract, entry_point="transfer").open_some(), paramCall)
        self.data.userStakeFlexPack[sp.sender].reward += self.getReward(sp.record(start = self.data.userStakeFlexPack[sp.sender].timestamp, end = sp.now.add_seconds(0), value = self.data.userStakeFlexPack[sp.sender].value, rate = self.data.stakingOptions[0].stakingPercentage))

        
        self.data.userStakeFlexPack[sp.sender].value = sp.as_nat(self.data.userStakeFlexPack[sp.sender].value - params.amount) 
        self.data.userStakeFlexPack[sp.sender].timestamp = sp.now.add_seconds(0)
        
        self.data.stakingHistory[sp.now.add_seconds(0)] = -1 * sp.to_int(params.amount)
        self.delStaker(sp.sender)
        
        
    # Use this function before updating the staking flex rate    
    @sp.entry_point
    def updateStakingFlexRate(self, params):
        sp.set_type(params, sp.TRecord(ad = sp.TList(sp.TAddress), rate = sp.TNat))
        
        sp.verify(sp.sender == self.data.admin, Error.NotAdmin)

        sp.for i in params.ad:

            self.data.userStakeFlexPack[i].reward += self.getReward(sp.record(start = self.data.userStakeFlexPack[i].timestamp, end = sp.now.add_seconds(0), value = self.data.userStakeFlexPack[i].value, rate = self.data.stakingOptions[0].stakingPercentage))
           
            self.data.userStakeFlexPack[i].timestamp = sp.now


    

    # The function claimRewardFlex will send the rewards of a staking flex to the user
    # the function takes no parameter
    @sp.entry_point
    def claimRewardFlex(self):
        sp.verify(self.data.userStakeFlexPack.contains(sp.sender), Error.NeverStaked)
        
        staking= self.data.userStakeFlexPack[sp.sender] 
        self.data.userStakeFlexPack[sp.sender].reward += self.getReward(sp.record(start = staking.timestamp, end = sp.now.add_seconds(0), value = staking.value, rate = self.data.stakingOptions[0].stakingPercentage))
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=self.data.userStakeFlexPack[sp.sender].reward)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        sp.if self.data.userStakeFlexPack[sp.sender].value == 0:
            del self.data.userStakeFlexPack[sp.sender]
        sp.else:
            self.updateRedeemedRewards(sp.sender, self.data.userStakeFlexPack[sp.sender].reward)
            self.data.userStakeFlexPack[sp.sender].reward = sp.as_nat(0) 
            self.data.userStakeFlexPack[sp.sender].timestamp = sp.now.add_seconds(0)



    # The function will compute the rewards for a specified value during a period at a certain rate
    # The function takes as parameters:
    # - the starting timestamp
    # - the ending timestamp
    # - the value of the staking
    # - the rate of the staking
    def getReward(self, params):
        sp.set_type(params, sp.TRecord(start=sp.TTimestamp, end = sp.TTimestamp, value= sp.TNat, rate=sp.TNat))
        k = sp.nat(10000000000)
        period = params.end - params.start
        timeRatio = k * sp.as_nat(period) / sp.as_nat(sp.timestamp(0).add_days(365) - sp.timestamp(0))
        reward = timeRatio * params.rate
        reward *= params.value
        reward /= k*100
        return reward
        
    @sp.utils.view(sp.TMap(sp.TNat, sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat)))
    def getStakingOptions(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.stakingOptions)
            
    @sp.utils.view(sp.TAddress)
    def getAdmin(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.admin)
        
    @sp.utils.view(sp.TAddress)
    def getReserve(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.reserve)
        
    @sp.utils.view(sp.TAddress)
    def getTokenContractAddress(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.FA12TokenContract)
        
    @sp.utils.view(sp.TAddress)
    def getVotingContract(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.votingContract.open_some(message = None))

        
    @sp.utils.view(sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock)))
    def getLockStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
        sp.if self.data.userStakeLockPack.contains(params):
            sp.result(self.data.userStakeLockPack[params])
        sp.else:
            sp.failwith("There is no locked staking for this address")
            
    @sp.utils.view(StakeFlex)
    def getFlexStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
        sp.if self.data.userStakeFlexPack.contains(params):
            sp.result(self.data.userStakeFlexPack[params])
        sp.else:
            sp.failwith("There is no flexible staking for this address")
            
    @sp.utils.view(sp.TNat)
    def getCurrentPendingRewards(self, params):
        sp.set_type(params, sp.TAddress)
        x = sp.local("x", sp.nat(0))
        sp.if self.data.userStakeFlexPack.contains(params):
            userFlexMap = self.data.userStakeFlexPack[params]
            x.value = x.value + userFlexMap.reward + self.getReward(sp.record(start = userFlexMap.timestamp, end = sp.now.add_seconds(0), value = userFlexMap.value, rate = self.data.stakingOptions[0].stakingPercentage))
        
        sp.if self.data.userStakeLockPack.contains(params):
            sp.for pack_id in self.data.userStakeLockPack[params].keys():
                sp.for item in self.data.userStakeLockPack[params].get(pack_id).values():
                    computed_end = item.timestamp.add_seconds(self.data.stakingOptions[pack_id].stakingPeriod)
                    sp.if computed_end < sp.now:
                        x.value = x.value + self.getReward(sp.record(start = item.timestamp, end = computed_end, value = item.value, rate = item.rate))
        sp.result(x.value)


            
class FA12Staking(FA12Staking_core, FA12Staking_methods):
    def __init__(self, contract, admin, reserve, metadata_url):
        FA12Staking_core.__init__(self, contract, admin, reserve,metadata_url)

            
class Viewer(sp.Contract):
    def __init__(self, t):
        self.init(last = sp.none)
        self.init_type(sp.TRecord(last = sp.TOption(t)))
    @sp.entry_point
    def target(self, params):
        self.data.last = sp.some(params)

@sp.add_test(name="Minimal")
def test():
    scenario = sp.test_scenario()
    scenario.h1("FA1.2 Staking contract")
    scenario.table_of_contents()

    # sp.test_account generates ED25519 key-pairs deterministically:
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob = sp.test_account("Robert")
    reserve = sp.test_account("Reserve")
    new_reserve = sp.test_account("New_Reserve")
    

    # Let's display the accounts:
    scenario.h1("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h1("Initialize the contract")
    contract = sp.address("KT1TezoooozzSmartPyzzSTATiCzzzwwBFA1")
    metadata_url = sp.utils.bytes_of_string("ipfs://Qmd24eKvMaYzBxbKEH6kr6nnnHMCCchntVprK3NJJfVvky")
    c1 = FA12Staking(contract, admin.address, reserve.address, metadata_url)
    scenario += c1

    scenario.h1("Tests")
    scenario.h2("Updating FA12TokenContract")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateContract(contract=sp.address("KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC")).run(sender=alice, valid=False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateContract(contract=sp.address("KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC")).run(sender=admin)

    scenario.h2("Updating reserve")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateReserve(reserve = new_reserve.address).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateReserve(reserve = new_reserve.address).run(sender = admin)
    
    scenario.h2("Creating a new staking option")
    scenario.h3("Alice tries to create a new staking option but does not succeed")
    scenario += c1.createStakingOption(_id = 0, rate = 20, _max = 1000000000000, _min = 0, duration = 0).run(sender = alice, valid = False)
    scenario.h3("Admin creates a new staking option that already exists")
    scenario += c1.createStakingOption(_id = 0, rate = 20, _max = 1000000000000, _min = 0, duration = 0).run(sender = admin, valid = False)
    scenario.h3("Admin creates a new staking option")
    scenario += c1.createStakingOption(_id = 1, rate = 20, _max = 1000000000000, _min = 10, duration = 31536000).run(sender = admin)
    scenario.h3("Admin creates a new staking option")
    scenario += c1.createStakingOption(_id = 2, rate = 20, _max = 1000000000000, _min = 10, duration = 31536000).run(sender = admin)
    
    scenario.h2("Updating MaxStake")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateStakingOptionMax(_id = 0, _max = 1000000).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateStakingOptionMax(_id = 0, _max = 1000000).run(sender = admin)

    scenario.h2("Updating MinStake")
    scenario += c1.updateStakingOptionMin(_id = 0, _min = 1000).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateStakingOptionMin(_id = 0, _min = 1000).run(sender = admin)

    scenario.h2("Updating staking duration")
    scenario += c1.updateStakingOptionDuration(_id = 0, duration = 10000).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateStakingOptionDuration(_id = 0, duration = 10000).run(sender = admin)

    scenario.h2("Updating staking rate")
    scenario.h3("Alice tries to update a staking pack rate")
    scenario += c1.updateStakingOptionRate(_id = 1, rate = 8).run(sender = alice, valid = False)
    scenario.h3("Admin tries to updates the staking flex rate but fails because he doesn't use the good function")
    scenario += c1.updateStakingOptionRate(_id = 0, rate = 8).run(sender = admin)
    scenario.h3("Admin updates a staking pack rate")
    scenario += c1.updateStakingOptionRate(_id = 1, rate = 8).run(sender = admin)
    
    scenario.h2("Updating Admin")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=alice, valid=False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=admin)

    scenario.h2("Staking flex")
    scenario.h3("Alice tries to stake flex and succeeds")
    scenario += c1.stakeFlex(amount = 10000).run(sender=alice)
    scenario.h3("Alice tries to stake more tokens and succeds")
    scenario += c1.stakeFlex(amount = 10100).run(sender = alice)
    scenario.h3("Admin tries to stake tokens and succeds")
    scenario += c1.stakeFlex(amount = 10000).run(sender = admin)
    
    scenario.h2("Changing the staking flex's rate")
    scenario.h3("The staking flex rate is changed")
    scenario += c1.updateStakingFlexRate(sp.record(ad = sp.list([sp.address("tz1WxrQuZ4CK1MBUa2GqUWK1yJ4J6EtG1Gwi"), sp.address("tz1hdQscorfqMzFqYxnrApuS5i6QSTuoAp3w")]), rate = 100)).run(sender = alice, now = sp.timestamp(int(31536000/2)))
    scenario.h3("An address that never staked is passed as argument so it fails")
    scenario += c1.updateStakingFlexRate(sp.record(ad = sp.list([sp.address("tz1WxrQuZ4CK1MBUa2GqUWK1yJ4J6EtG1Gww")]), rate = 12)).run(sender = alice, valid = False, now = sp.timestamp(int(31536000/2)))
    scenario.h3("Trying to update the staking flex rate but is not admin nor voting contract")
    scenario += c1.updateStakingFlexRate(sp.record(ad = sp.list([sp.address("tz1WxrQuZ4CK1MBUa2GqUWK1yJ4J6EtG1Gwi")]), rate = 12)).run(sender = bob, valid = False, now = sp.timestamp(int(31536000/2)))
    
    
    
    scenario.h3("Alice tries to stake too few tokens and fails")
    scenario += c1.stakeFlex(amount = 1).run(sender = alice, valid = False)
    scenario.h3("Alice tries to stake too much tokens and fails")
    scenario += c1.stakeFlex(amount = 1000001).run(sender = alice, valid = False)
    scenario.h3("Alice tries to stake more tokens and succeds")
    scenario += c1.stakeFlex(amount = 10000).run(sender = alice)
    
    
    scenario.h2("Unstaking flex")
    scenario.h3("Alice tries to unstake some of her tokens after 1 year and succeeds")
    scenario += c1.unstakeFlex(amount = 100).run(sender = alice, now = sp.timestamp(31536000))
    scenario.h3("Admin tries to unstake all of her tokens after 1 year and succeds")
    scenario += c1.unstakeFlex(amount = 10000).run(sender = admin, now = sp.timestamp(31536000))
    scenario.h3("Alice tries to unstake all of her tokens after 1 year and succeds")
    scenario += c1.unstakeFlex(amount = 20000).run(sender = alice, now = sp.timestamp(2*31536000))
    scenario.h3("Alice tries to unstake tokens even though she has already unstaked everything")
    scenario += c1.unstakeFlex(amount = 1000).run(sender = alice, now = sp.timestamp(31536000), valid = False)
    scenario.h3("Bob tries to unstake but he never staked")
    scenario += c1.unstakeFlex(amount = 1000).run(sender = bob, valid = False)
    
    
    scenario.h2("Staking flex reward claiming")
    scenario.h3("Alice claims her rewards for her past stakings and succeeds (watch console)")
    scenario += c1.claimRewardFlex().run(sender = alice, now = sp.timestamp(2*31536000))
    scenario.h3("Admin claims her rewards for her past stakings and succeeds (watch console)")
    scenario += c1.claimRewardFlex().run(sender = admin, now = sp.timestamp(2*31536000))
    scenario.h3("Alice tries to claim her rewards again but since she has no token staked she gets no rewards (watch console)")
    scenario += c1.claimRewardFlex().run(sender = alice, now = sp.timestamp(3*31536000))
    scenario.h3("Bob tries to claim rewards but he never stake and he fails")
    scenario += c1.claimRewardFlex().run(sender = bob, valid = False)
    
    
    scenario.h2("Staking lock")
    scenario.h3("Alice tries to stake using the locked pack 1 and succeeds")
    scenario += c1.stakeLock(pack = 1, amount = 10000).run(sender = alice, now = sp.timestamp(10))
    scenario.h3("Alice tries to create another stake for the same pack and succeds")
    scenario += c1.stakeLock(pack = 1, amount = 10000).run(sender = alice)
    scenario.h3("Alice tries to stake too few tokens for the pack 1 and fails")
    scenario += c1.stakeLock(pack = 1, amount = 1).run(sender = alice, valid = False)
    scenario.h3("Alice tries to stake too much tokens for the pack 1 and fails")
    scenario += c1.stakeLock(pack = 1, amount = 1000000000001).run(sender = alice, valid = False)
    scenario.h3("Alice tries to stake using the locked pack 3 that doesn't exist and fails")
    scenario += c1.stakeLock(pack = 3, amount = 100000).run(sender = alice, valid = False)
    
    
    scenario.h2("Unstaking lock")
    scenario.h3("Alice tries to unstake her tokens before the end of the locking period and does not get her rewards (watch console)")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender = alice, now = sp.timestamp(31535999))
    scenario.h3("Alice tries to unstake her tokens after the locking period and gets here rewards (watch console)")
    scenario += c1.unstakeLock(pack = 1, index = 1).run(sender = alice, now = sp.timestamp(31536011))
    scenario.h3("Alice tries to unstake and already unstaked staking and fails")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender = alice, now = sp.timestamp(31536001), valid = False)
    scenario.h3("Alice tries to unstake a pack she never used and fails")
    scenario += c1.unstakeLock(pack = 2, index = 0).run(sender = alice, valid = False)
    scenario.h3("Alice tries to unstake a pack that doesn't exist and fails")
    scenario += c1.unstakeLock(pack = 3, index = 0).run(sender = alice, valid = False)
    scenario.h3("Bob tries to unstake but he has never staked and fails")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender = bob, valid = False)
    
    scenario.h3("Alice stakes again a locked pack")
    scenario += c1.stakeLock(pack = 1, amount = 100000).run(sender = alice)
    scenario.h3("Alice stakes again in flex pack")
    scenario += c1.stakeFlex(amount = 10000).run(sender=alice, now = sp.timestamp(94608000))
    
    scenario.h2("Attempt to update metadata")
    c1.updateMetadata(url = sp.bytes("0x00")).run(sender = alice)
    scenario.verify(c1.data.metadata[""] == sp.bytes("0x00"))
    
    scenario.h2("Purging staking history")
    c1.purgeStakingHistory(timestamp_list = sp.list([sp.timestamp(0), sp.timestamp(10), sp.timestamp(15768000)])).run(sender=alice)
    """scenario.h1("Views")
    scenario.h2("Administrator")
    view_administrator = Viewer(sp.TAddress)
    scenario += view_administrator
    c1.getAdmin((sp.unit, view_administrator.typed.target))
    scenario.verify_equal(view_administrator.data.last, sp.some(alice.address))
    
    scenario.h2("Staking options")
    scenario.h3("List all staking options")
    view_staking_options = Viewer(sp.TMap(sp.TNat, sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat)))
    scenario += view_staking_options
    c1.getStakingOptions((sp.unit, view_staking_options.typed.target))
    scenario.verify_equal(view_staking_options.data.last, sp.some(sp.map({0:sp.record(minStake = 1000, maxStake = 1000000, stakingPercentage = 8, stakingPeriod = 10000), 1: sp.record(minStake = 10, maxStake = 1000000000000, stakingPercentage = 20, stakingPeriod = 31536000), 2: sp.record(minStake = 10, maxStake = 1000000000000, stakingPercentage = 20, stakingPeriod = 31536000)})))
    
    scenario.h2("Tokens reserve")
    view_reserve = Viewer(sp.TAddress)
    scenario += view_reserve
    c1.getReserve((sp.unit, view_reserve.typed.target))
    scenario.verify_equal(view_reserve.data.last, sp.some(new_reserve.address))
    
    scenario.h2("Token contract address")
    view_token_contract = Viewer(sp.TAddress)
    scenario += view_token_contract
    c1.getTokenContractAddress((sp.unit, view_token_contract.typed.target))
    scenario.verify_equal(view_token_contract.data.last, sp.some(sp.address("KT1Tezooo3zzSmartPyzzSTATiCzzzseJjWC")))
    
    scenario.h2("Flex staking")
    scenario.h3("Flex staking information for a given address")
    view_staking_flex = Viewer(sp.TRecord(timestamp=sp.TTimestamp, value=sp.TNat, reward=sp.TNat))
    scenario += view_staking_flex
    c1.getFlexStakeInformation((alice.address, view_staking_flex.typed.target))
    scenario.verify_equal(view_staking_flex.data.last, sp.some(sp.record(timestamp = sp.timestamp(94608000), value = 10000, reward = 0)))
    
    scenario.h2("Lock staking")
    scenario.h3("List all locked stakes")
  
    scenario.h3("Locked staking information for a given address")
    view_staking_lock = Viewer(sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock)))
    scenario += view_staking_lock
    c1.getLockStakeInformation((alice.address, view_staking_lock.typed.target))
    scenario.verify_equal(view_staking_lock.data.last, sp.some(sp.map({1:sp.map({0:sp.record(rate = 20, timestamp = sp.timestamp(31536001), value = 100000)})})))
    
    scenario.h2("Get current pending total rewards")
    view_current_rewards = Viewer(sp.TNat)
    scenario += view_current_rewards
    c1.getCurrentPendingRewards((alice.address, view_current_rewards.typed.target)).run(now = sp.timestamp(94708000))
    scenario.verify_equal(view_current_rewards.data.last, sp.some(sp.nat(20002)))"""
