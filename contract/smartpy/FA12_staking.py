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


StakeLock = sp.TRecord(
    timestamp=sp.TTimestamp,
    rate=sp.TNat,
    value=sp.TNat
)

StakeFlex = sp.TRecord(
    timestamp=sp.TTimestamp,
    rate=sp.TNat,
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

Options = sp.big_map(
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


class FA12Staking(sp.Contract):
    def __init__(self, contract, admin, reserve, **kargs):
        self.init(
            FA12TokenContract=contract,
            admin=admin,
            reserve=reserve,
            userStakeLockPack=UserStakeLockPack,
            userStakeFlexPack=UserStakeFlexPack,
            totalReward = TotalReward
            stakingOptions=Options,
            votingContract = sp.none,
            **kargs
        )

    @sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.reserve = params.reserve

    @sp.entry_point
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.admin = params.admin
        
    @sp.entry_point
    def updateContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin, Error.NotAdmin)
        self.data.FA12TokenContract = params.contract
    
    
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
        
    @sp.entry_point
    def updateStakingOptionRate(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat).layout(("_id as id", "rate")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].stakingPercentage = params.rate

    @sp.entry_point
    def updateStakingOptionDuration(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, duration = sp.TInt).layout(("_id as id", "duration")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].stakingPeriod = params.duration
        
    @sp.entry_point
    def updateStakingOptionMax(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _max = sp.TNat).layout(("_id as id", "_max as max")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].maxStake = params._max
        
    @sp.entry_point
    def updateStakingOptionMin(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _min = sp.TNat).layout(("_id as id", "_min as min")))
        sp.verify(self.is_voting_contract(sp.sender) | (self.data.admin == sp.sender), Error.NotAdmin)
        sp.verify(self.data.stakingOptions.contains(params._id), Error.NotStakingOpt)
        self.data.stakingOptions[params._id].minStake = params._min
    
    def initUserStaking(self, addr, pack, staking):
        self.data.userStakeLockPack[addr] = sp.map({pack:sp.map({0:staking})})
    
    def addStaking(self, addr, pack, staking):
        self.data.userStakeLockPack[addr][pack][sp.len(self.data.userStakeLockPack[addr][pack])]= staking
    
    def addStakingPack(self, addr, pack, staking):
        self.data.userStakeLockPack[addr][pack]= sp.map({0:staking})
    
    @sp.entry_point
    def stake(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, amount = sp.TNat))
        sp.verify(params.amount > self.data.stakingOptions[params.pack].minStake, Error.AmountTooLow)
        sp.verify(params.amount < self.data.stakingOptions[params.pack].maxStake, Error.AmountTooHigh)
        staking = sp.record(timestamp=sp.now, rate = self.data.stakingOptions[params.pack].stakingPercentage, value = params.amount)
        sp.if ~self.data.userStakeLockPack.contains(sp.sender):
            self.initUserStaking(sp.sender, params.pack, staking)
        sp.else:
            sp.if ~self.data.userStakeLockPack[sp.sender].contains(params.pack):
                self.addStakingPack(sp.sender, params.pack, staking)
            sp.else:
                self.addStaking(sp.sender, params.pack, staking)


    @sp.entry_point
    def unstakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack=sp.TNat, index=sp.TNat))
        """ on vérifie que le sender a bien deja staké """
        sp.verify(self.data.userStakeLockPack.contains(sp.sender), Error.NeverStaked)
        """ on vérifie que le sender a deja staké le pack qu'il veut redeem """
        sp.verify(self.data.userStakeLockPack[sp.sender].contains(params.pack), Error.NeverUsedPack)
        """ on vérifie que le staking qu'il veut withdraw existe """
        sp.verify(sp.len(self.data.userStakeLockPack[sp.sender][params.pack]) > params.index, Error.NotStaking)
        amount = sp.nat(0)
        sp.if (self.data.userStakeLockPack[sp.sender][params.pack][params.index].timestamp.add_days(self.data.stakingOptions[params.pack].stakingPeriod) < sp.now):
            amount = self.getReward(self.data.userStakeLockPack[sp.sender][params.pack][params.index], self.data.userStakeLockPack[sp.sender][params.pack][params.index].timestamp.add_seconds(self.data.stakingOptions[params.pack].stakingPeriod)) + self.data.userStakeLockPack[sp.sender][params.pack][params.index].value
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract,entry_point="transfer").open_some(), paramCall)
        del self.data.userStakeLockPack[sp.sender][params.pack][params.index]


    @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TNat)
        """ on vérifie que le sender a bien deja staké """
        sp.verify(self.data.userStakeLockPack.contains(sp.sender), Error.NeverStaked)
        """ on vérifie que le sender a deja staké le pack qu'il veut redeem """
        sp.verify(self.data.userStakeLockPack[sp.sender][0].contains(params), Error.NeverUsedPack)

        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=self.getReward(self.data.userStakeLockPack[sp.sender][0][params], sp.now))
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        del self.data.userStakeLockPack[sp.sender][0][params]

    def getReward(self, stake, end):
        k = sp.nat(10000000000)
        period = end - stake.timestamp
        timeRatio = k * sp.as_nat(period) / sp.as_nat(sp.timestamp(1).add_days(365) - sp.timestamp(1))
        reward = timeRatio * stake.rate
        reward *= stake.value
        reward /= k*100
        return reward


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

    # Let's display the accounts:
    scenario.h1("Accounts")
    scenario.show([admin, alice, bob])

    scenario.h1("Initialize the contract")
    contract = sp.address("KT11...")
    c1 = FA12Staking(contract, admin.address, reserve.address)
    scenario += c1

    scenario.h1("Tests")
    scenario.h2("Updating FA12TokenContract")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateContract(contract=sp.address("KT12...")).run(sender=alice, valid=False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateContract(contract=sp.address("KT12...")).run(sender=admin)

    scenario.h2("Updating reserve")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateReserve(reserve = sp.address("KT13reserve...")).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateReserve(reserve = sp.address("KT13reserve...")).run(sender = admin)
    
    scenario.h2("Creating a new staking option")
    scenario.h3("Alice tries to create a new staking option but does not succeed")
    scenario += c1.createStakingOption(_id = 0, rate = 20, _max = 1000000000000, _min = 0, duration = 0).run(sender = alice, valid = False)
    scenario.h3("Admin creates a new staking option")
    scenario += c1.createStakingOption(_id = 0, rate = 20, _max = 1000000000000, _min = 0, duration = 0).run(sender = admin)
    scenario.h3("Admin creates a new staking option")
    scenario += c1.createStakingOption(_id = 1, rate = 20, _max = 1000000000000, _min = 0, duration = 31536000).run(sender = admin)
    
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
    scenario += c1.updateStakingOptionRate(_id = 0, rate = 8).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateStakingOptionRate(_id = 0, rate = 8).run(sender = admin)
    
    scenario.h2("Updating Admin")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=alice, valid=False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=admin)

    scenario.h2("Staking flex")
    scenario.h3("Alice tries to stake flex and succeeds")
    scenario += c1.stake(pack=0, amount = 10000).run(sender=alice)
    scenario.h3("Alice tries to stake on the same pack")
    scenario += c1.stake(pack=0, amount = 100000).run(sender=alice)
    
    scenario.h2("Unstaking flex")
    scenario.h3("Alice tries to unstake and succeeds")
    scenario += c1.unstakeFlex(0).run(sender=alice)
    scenario.h3("Alice tries to unstake a staking she didn't make and fails")
    scenario += c1.unstakeFlex(2).run(sender=alice, valid = False)
    scenario.h3("Alice tries to unstake the 2nd stake and succeeds")
    scenario += c1.unstakeFlex(1).run(sender=alice)
    
    scenario.h2("Staking lock")
    scenario.h3("Alice tries to stake Lock and succeeds")
    scenario += c1.stake(pack = 1, amount = 100).run(sender=alice)
    scenario.h3("Alice tries to stake a pack that doesn't exist and fails")
    scenario += c1.stake(pack = 2, amount = 10000).run(sender = alice, valid = False)
    
    scenario.h2("Unstaking lock")
    scenario.h3("Alice tries to unstake a lock pack and succeeds")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender= alice)
    scenario.h3("Alice tries to unstake a pack she didn't use and fails")
    scenario += c1.unstakeLock(pack=2, index=3).run(sender=alice, valid = False)
    scenario.h3("Alice tries to unstake a stake she didn't use and fails")
    scenario += c1.unstakeLock(pack=1, index=3).run(sender=alice, valid = False)
    
    
   
