import smartpy as sp

"""---------------------------------------------------------------------"""
# TODO On considère le staking lock comme 0 et le staking flex comme 1
"""---------------------------------------------------------------------"""
Stake = sp.TRecord(
    timestamp=sp.TTimestamp,
    rate=sp.TInt,
    value=sp.TInt
)

UserStakePack = sp.big_map(
    tkey = sp.TAddress,
    tvalue = sp.TMap(
       sp.TNat,
       sp.TMap(
           sp.TNat,
           Stake)
    )
)

Options = sp.big_map(
    tkey = sp.TNat,
    tvalue = sp.TRecord(
        minStake = sp.TNat,
        maxStake = sp.TNat,
        stakingPeriod = sp.TNat,
        stakingPercentage = sp.TNat
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
            userStakePack = UserStakePack,
            stakingOptions = Options,
            votingContract = sp.none,
            **kargs
        )

    @sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.reserve = params.reserve

    @sp.entry_point
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.admin = params.admin
        
    @sp.entry_point
    def updateContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.FA12TokenContract = params.contract
    
    @sp.entry_point
    def updateVotingContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.votingContract = sp.some(params.contract)
        
    def is_voting_contract(self, contract):
        #sp.trace(self.data.votingContract.is_some())
        a = sp.bool(False)
        sp.if -self.data.votingContract.is_some():
            return "plop"
        sp.else:
            return "blblb"
            
    
    def t(self):
        if False:
            return "op"
        else:
            return "ko"
    @sp.entry_point
    def updateOptionPackPercentage(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, percentage = sp.TNat))
        #sp.verify(self.is_voting_contract(sp.sender))
        #sp.trace(self.is_voting_contract(sp.sender))
        period = sp.now.add_days(90)-sp.timestamp(0)
        period2 = sp.timestamp(0).add_days(365)-sp.timestamp(0)
        timeRatio =sp.nat(100000)*sp.as_nat(period) /sp.as_nat(period2)
        sp.trace(timeRatio)
        
        #sp.trace(self.t())
        #sp.verify(sp.sender == self.data.votingContract.open_some())
        
    

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

    scenario.h2("Updating Admin")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=alice, valid=False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateAdmin(admin=alice.address).run(sender=admin)

    scenario.h2("Updating MaxStake")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario.h3("Admin updates the state variable")

    scenario.h2("Updating MinStake")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario.h3("Admin updates the state variable")

    scenario.h2("Updating reserve")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario.h3("Admin updates the state variable")

    scenario.h2("Updating staking percentage")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario.h3("Admin updates the state variable")

    scenario.h2("Updating staking period")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario.h3("Admin updates the state variable")
    
    
    scenario += c1.updateOptionPackPercentage(_id = sp.nat(5), percentage =  sp.nat(4)).run(sender=admin)
