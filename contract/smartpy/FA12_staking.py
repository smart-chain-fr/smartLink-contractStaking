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


StakeLock = sp.TRecord(
    timestamp=sp.TTimestamp,
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

Options = sp.big_map(
    tkey=sp.TNat,
    tvalue= sp.TRecord(
            minStake=sp.TNat,
            maxStake=sp.TNat,
            stakingPeriod=sp.TInt,
            stakingPercentage=sp.TNat
        )
    )

TZIP16_Metadata_Base = {
    "name"          : "SMAK Staking",
    "description"   : "SMAK Staking smart-contract",
    "authors"       : [
        "Smartlink Dev Team <email@domain.com>"
    ],
    "homepage"      : "https://smartpy.io",
    "interfaces"    : [
        "TZIP-007-2021-04-17",
        "TZIP-016-2021-04-17"
    ],
}

def call(c, x):
    sp.transfer(x, sp.mutez(0), c)

class FA12Staking_config:
    def __init__(
        self,
        support_upgradable_metadata         = False,
        use_token_metadata_offchain_view    = True,
    ):
        self.support_upgradable_metadata = support_upgradable_metadata
        # Whether the contract metadata can be upgradable or not.
        # When True a new entrypoint `change_metadata` will be added.

        self.use_token_metadata_offchain_view = use_token_metadata_offchain_view
        # Include offchain view for accessing the token metadata (requires TZIP-016 contract metadata)

class FA12Staking_common:
    def normalize_metadata(self, metadata):
        """
            Helper function to build metadata JSON (string => bytes).
        """
        for key in metadata:
            metadata[key] = sp.utils.bytes_of_string(metadata[key])

        return metadata
        
class FA12Staking_core(sp.Contract, FA12Staking_common):
    def __init__(self, contract, admin, reserve, config, **kargs):
        
        self.config = config
        self.init(
            FA12TokenContract=contract,
            admin=admin,
            reserve=reserve,
            userStakeLockPack=UserStakeLockPack,
            userStakeFlexPack=UserStakeFlexPack,
            totalReward = TotalReward,
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
  

class FA12Staking_methods(FA12Staking_core):
    
    def getReward(self, start, end, value, rate):
        k = sp.nat(10000000000)
        period = end - start
        timeRatio = k * sp.as_nat(period) / sp.as_nat(sp.timestamp(1).add_days(365) - sp.timestamp(1))
        reward = timeRatio * rate
        reward *= value
        reward /= k*100
        return reward
        
    def updateStakingFlex(self, addr, amount):
        self.data.userStakeFlexPack[addr].reward = self.getReward(self.data.userStakeFlexPack[addr].timestamp, sp.now.add_seconds(0), self.data.userStakeFlexPack[addr].value, self.data.stakingOptions[0].stakingPercentage)
        self.data.userStakeFlexPack[addr].value += amount
        self.data.userStakeFlexPack[addr].timestamp = sp.now.add_seconds(0)
        
    @sp.entry_point
    def stakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, amount = sp.TNat))
        
        sp.verify(params.amount > self.data.stakingOptions[params.pack].minStake, Error.AmountTooLow)
        sp.verify(params.amount < self.data.stakingOptions[params.pack].maxStake, Error.AmountTooHigh)
        sp.verify(self.data.stakingOptions.contains(params.pack), Error.NotStakingOpt)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=sp.sender, to_=self.data.reserve, value=params.amount)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        
        staking = sp.record(timestamp=sp.now.add_seconds(0), rate = self.data.stakingOptions[params.pack].stakingPercentage, value = params.amount)
        sp.if ~self.data.userStakeLockPack.contains(sp.sender):
            self.data.userStakeLockPack[sp.sender] = sp.map({params.pack :sp.map(l= {sp.nat(0):staking})})
        sp.else:
            sp.if ~self.data.userStakeLockPack[sp.sender].contains(params.pack):
                self.data.userStakeLockPack[sp.sender][params.pack] = sp.map({sp.nat(0):staking})
            sp.else:
                index = sp.len(self.data.userStakeLockPack[sp.sender][params.pack])
                self.data.userStakeLockPack[sp.sender][params.pack][index] = staking

    @sp.entry_point
    def stakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
        sp.verify(params.amount > self.data.stakingOptions[0].minStake, Error.AmountTooLow)
        sp.verify(params.amount < self.data.stakingOptions[0].maxStake, Error.AmountTooHigh)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=sp.sender, to_=self.data.reserve, value=params.amount)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        
        sp.if ~self.data.userStakeFlexPack.contains(sp.sender):
            self.data.userStakeFlexPack[sp.sender] = sp.record(timestamp = sp.now.add_seconds(0), value = params.amount + sp.nat(0), reward = sp.nat(0))
        sp.else:
            self.updateStakingFlex(sp.sender, params.amount)

    @sp.entry_point
    def unstakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack=sp.TNat, index=sp.TNat))
        
        sp.verify(self.data.stakingOptions.contains(params.pack), Error.NotStakingOpt)
        sp.verify(self.data.userStakeLockPack.contains(sp.sender), Error.NeverStaked)
        sp.verify(self.data.userStakeLockPack[sp.sender].contains(params.pack), Error.NeverUsedPack)
        sp.verify(self.data.userStakeLockPack[sp.sender][params.pack].contains(params.index), Error.NotStaking)
        
        amount = sp.nat(0)
        sp.if (self.data.userStakeLockPack[sp.sender][params.pack][params.index].timestamp.add_seconds(self.data.stakingOptions[params.pack].stakingPeriod) < sp.now.add_seconds(0)):
            staking = self.data.userStakeLockPack[sp.sender][params.pack][params.index]
            amount = self.getReward(staking.timestamp, staking.timestamp.add_seconds(self.data.stakingOptions[params.pack].stakingPeriod), staking.value, staking.rate) + staking.value
            
        """TRACE VERIFY REWARDS"""
        #sp.trace(amount)
        """TRACE VERIFY REWARDS"""
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract,entry_point="transfer").open_some(), paramCall)
        del self.data.userStakeLockPack[sp.sender][params.pack][params.index]


    @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
        
        sp.verify(self.data.userStakeFlexPack.contains(sp.sender), Error.NeverStaked)
        sp.verify(self.data.userStakeFlexPack[sp.sender].value >= params.amount, Error.BalanceTooLow)
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=params.amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract, entry_point="transfer").open_some(), paramCall)
        
        self.data.userStakeFlexPack[sp.sender].reward += self.getReward(self.data.userStakeFlexPack[sp.sender].timestamp, sp.now.add_seconds(0), self.data.userStakeFlexPack[sp.sender].value, self.data.stakingOptions[0].stakingPercentage)
        
        
        
        self.data.userStakeFlexPack[sp.sender].value = sp.as_nat(self.data.userStakeFlexPack[sp.sender].value - params.amount) 
        self.data.userStakeFlexPack[sp.sender].timestamp = sp.now.add_seconds(0)
        
    @sp.entry_point
    def claimRewardFlex(self):
        sp.verify(self.data.userStakeFlexPack.contains(sp.sender), Error.NeverStaked)
        
        staking= self.data.userStakeFlexPack[sp.sender] 
        self.data.userStakeFlexPack[sp.sender].reward += self.getReward(staking.timestamp, sp.now.add_seconds(0), staking.value, self.data.stakingOptions[0].stakingPercentage)
        
        """TRACE VERIFY REWARDS"""
        sp.trace(staking)
        """TRACE VERIFY REWARDS"""
        
        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, value=self.data.userStakeFlexPack[sp.sender].reward)
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
        
        self.data.userStakeFlexPack[sp.sender].reward = sp.as_nat(0) 
        self.data.userStakeFlexPack[sp.sender].timestamp = sp.now.add_seconds(0)

    def getReward(self, start, end, value, rate):
        k = sp.nat(10000000000)
        period = end - start
        timeRatio = k * sp.as_nat(period) / sp.as_nat(sp.timestamp(0).add_days(365) - sp.timestamp(0))
        reward = timeRatio * rate
        reward *= value
        reward /= k*100
        return reward

class FA12_Staking_contract_metadata(FA12Staking_core):
    """
        SPEC: https://gitlab.com/tzip/tzip/-/blob/master/proposals/tzip-16/tzip-16.md

        This class offers utilities to define and set TZIP-016 contract metadata.
    """
    def generate_tzip16_metadata(self):
        metadata = {
            **TZIP16_Metadata_Base
        }

        self.init_metadata("metadata", metadata)

    def set_contract_metadata(self, metadata):
        """
           Set contract metadata
        """
        self.update_initial_storage(
            metadata = sp.big_map(self.normalize_metadata(metadata))
        )

        if self.config.support_upgradable_metadata:
            def update_metadata(self, key, value):
                """
                    An entry-point to allow the contract metadata to be updated.

                    Can be removed with `FA12_config(support_upgradable_metadata = False, ...)`
                """
                sp.verify_equal(self.data.admin, sp.sender, Error.NotAdmin)
                self.data.metadata[key] = value
            self.update_metadata = sp.entry_point(update_metadata)
            
class FA12Staking(FA12Staking_core, FA12_Staking_contract_metadata, FA12Staking_methods):
    def __init__(self, contract, admin, reserve, config, contract_metadata = None):
        FA12Staking_core.__init__(self, contract, admin, reserve, config)
        if contract_metadata is not None:
            self.set_contract_metadata(contract_metadata)
        # This is only an helper, it produces metadata in the output panel
        # that users can copy and upload to IPFS.
        self.generate_tzip16_metadata()
            
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
    contract_metadata = {}
    c1 = FA12Staking(contract, admin.address, reserve.address, config = FA12Staking_config(support_upgradable_metadata = True), contract_metadata = contract_metadata)
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
    scenario += c1.stakeFlex(amount = 10000).run(sender=alice)
    scenario.h3("Alice tries to stake more tokens and succeds")
    scenario += c1.stakeFlex(amount = 10100).run(sender = alice)
    scenario.h3("ALice tries to stake too few tokens and fails")
    scenario += c1.stakeFlex(amount = 1).run(sender = alice, valid = False)
    scenario.h3("Alice tries to stake too much tokens and fails")
    scenario += c1.stakeFlex(amount = 1000001).run(sender = alice, valid = False)
    
    
    scenario.h2("Unstaking flex")
    scenario.h3("Alice tries to unstake some of her tokens after 1 year and succeeds")
    scenario += c1.unstakeFlex(amount = 100).run(sender = alice, now = sp.timestamp(31536000))
    scenario.h3("Alice tries to unstake all of her tokens after 1 year and succeds")
    scenario += c1.unstakeFlex(amount = 20000).run(sender = alice, now = sp.timestamp(31536001))
    scenario.h3("Alice tries to unstake tokens even though she has already unstaked everything")
    scenario += c1.unstakeFlex(amount = 1000).run(sender = alice, now = sp.timestamp(31536000), valid = False)
    scenario.h3("Bob tries to unstake but he never staked")
    scenario += c1.unstakeFlex(amount = 1000).run(sender = bob, valid = False)
    
    scenario.h2("Staking flex reward claiming")
    scenario.h3("Alice claims her rewards for her past stakings and succeeds (watch console)")
    scenario += c1.claimRewardFlex().run(sender = alice, now = sp.timestamp(2*31536000))
    scenario.h3("Alice tries to claim her rewards again but since she has no token staked she gets no rewards (watch console)")
    scenario += c1.claimRewardFlex().run(sender = alice, now = sp.timestamp(3*31536000))
    scenario.h3("Bob tries to claim rewards but he never stake and he fails")
    scenario += c1.claimRewardFlex().run(sender = bob, valid = False)
    
    
    scenario.h2("Staking lock")
    scenario.h3("Alice tries to stake using the locked pack 1 and succeeds")
    scenario += c1.stakeLock(pack = 1, amount = 10000).run(sender = alice)
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
    scenario += c1.unstakeLock(pack = 1, index = 1).run(sender = alice, now = sp.timestamp(31536001))
    scenario.h3("Alice tries to unstake and already unstaked staking and fails")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender = alice, now = sp.timestamp(31536001), valid = False)
    scenario.h3("Alice tries to unstake a pack she never used and fails")
    scenario += c1.unstakeLock(pack = 2, index = 0).run(sender = alice, valid = False)
    scenario.h3("Alice tries to unstake a pack that doesn't exist and fails")
    scenario += c1.unstakeLock(pack = 3, index = 0).run(sender = alice, valid = False)
    scenario.h3("Bob tries to unstake but he has never staked and fails")
    scenario += c1.unstakeLock(pack = 1, index = 0).run(sender = bob, valid = False)
    
    scenario.h1("Attempt to update metadata")
    c1.update_metadata(key = "", value = sp.bytes("0x00")).run(sender = alice)
    scenario.verify(c1.data.metadata[""] == sp.bytes("0x00"))
