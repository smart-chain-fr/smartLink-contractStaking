import smartpy as sp

#Stake = sp.TRecord(
#            timestamp = sp.TTimestamp,
#            rate = sp.TInt,
#            value = sp.TInt
#        )

class FA12Staking(sp.Contract):
    def __init__(self, contract, admin, reserve, **kargs):
        # je pense que le "approvals = sp.TMap" est inutile ici, cf, voir plus haut!
        self.stake = sp.TRecord(
            approvals=sp.TMap(
                timestamp = sp.TTimestamp,
                rate = sp.TInt,
                value = sp.TInt)
        )
        
        self.userstakePack = sp.big_map(
            tkey = sp.TAddress,
            tvalue = sp.map(
                tkey = sp.Tint,
                tvalue = sp.Tlist(stake))
            )
                                   
        self.init(
            FA12TokenContract = contract,
            admin = admin, 
            reserve = reserve,
            minStake = minstake,
            maxStake = maxstake,
            stakingPeriod = period,
            stakingPercentage = percentage,
            **kargs
        )
                                
    @sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.reserve = params.reserve
    
    @sp.entry_point    
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin = sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.admin = params.admin
        
    @sp.entry_point
    def updateMinStake(self, params):
        sp.set_type(params, sp.TRecord(minstake = sp.TNat))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.minStake = params.minstake
    
    @sp.entry_point
    def updateMaxStake(self, params):
        sp.set_type(params, sp.TRecord(maxstake = sp.TNat))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.maxStake = params.maxstake
    
    @sp.entry_point
    def updatePercentage(self, params):
        sp.set_type(params, sp.TRecord(percentage = sp.TNat))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.stakingPercentage = params.percentage
        
    @sp.entry_point
    def updatePeriod(self, params):
        sp.set_type(params, sp.TRecord(period = sp.TNat))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.stakingPeriod = params.period
        
@sp.add_test(name = "Minimal")
def test():
    scenario = sp.test_scenario()
    scenario.h1("FA1.2 Staking contract")
    scenario.table_of_contents()
    
    # sp.test_account generates ED25519 key-pairs deterministically:
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Robert")
    reserve = sp.test_account("Reserve")
    
    # Let's display the accounts:
    scenario.h1("Accounts")
    scenario.show([admin, alice, bob])
    
    scenario.h1("Initialize the contract")
    contract = sp.address("KT11...")
    c1 = FA12Staking(contract, admin.address, reserve.address, sp.nat(0), sp.nat(10000), sp.nat(90), sp.nat(5))
    scenario += c1
    
    scenario.h1("Tests")
    scenario.h2("Updating FA12TokenContract")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateContract(contract = sp.address("KT12...")).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateContract(contract = sp.address("KT12...")).run(sender = admin)
    
    scenario.h2("Updating Admin")
    scenario.h3("Alice tries to update the state variable but does not succeed")
    scenario += c1.updateAdmin(admin = alice.address).run(sender = alice, valid = False)
    scenario.h3("Admin updates the state variable")
    scenario += c1.updateAdmin(admin = alice.address).run(sender = admin)
    
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
