import smartpy as sp


class FA12Staking(sp.Contract):
    def __init__(self, contract, admin, reserve, **kargs):
        
        self.stake = sp.TRecord(approvals=sp.TMap(
            timestamp = sp.TTimestamp,
            rate = sp.TInt,
            value = sp.TInt)
        
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
            **kargs
        )

    @sp.entry_point
    def entry_point_1(self):
        pass

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
    
    scenario.h1("Minimal")
    contract = sp.address("KT11...")
    c1 = FA12Staking(contract, admin.address, reserve.address)
    scenario += c1



