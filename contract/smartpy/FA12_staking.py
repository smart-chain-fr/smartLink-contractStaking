import smartpy as sp

"""---------------------------------------------------------------------"""
# TODO On considère le staking flex comme 0 et le staking lock comme 1
"""---------------------------------------------------------------------"""
Stake = sp.TRecord(
    timestamp=sp.TTimestamp,
    rate=sp.TInt,
    value=sp.TInt
)

UserStakePack = sp.big_map(
    tkey=sp.TAddress,
    tvalue=sp.TMap(
        sp.TNat,
        sp.TMap(
            sp.TNat,
            Stake)
    )
)

Options = sp.big_map(
    tkey=sp.TNat,
    tvalue=sp.TMap(
        sp.TNat,
        sp.TRecord(
            minStake=sp.TNat,
            maxStake=sp.TNat,
            stakingPeriod=sp.TNat,
            stakingPercentage=sp.TNat
        )
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
            userStakePack=UserStakePack,
            stakingOptions=Options,
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
        sp.set_type(params, sp.TRecord(contract=sp.TAddress))
        sp.verify_equal(sp.sender, self.data.admin)
        self.data.FA12TokenContract = params.contract

    @sp.entry_point
    def unstakeLock(self, params):
        """pack=sp.TNat,"""
        sp.set_type(params, sp.TPair(sp.TNat, sp.TNat))
        """ on vérifie que le sender a bien deja staké """
        sp.verify(self.data.userStakePack.contains(sp.sender))
        """ on vérifie que le sender a deja staké le pack qu'il veut redeem """
        sp.verify(self.data.userStakePack[sp.sender].contains(params[0]))
        """ on vérifie que le staking qu'il veut withdraw existe """
        sp.verify(sp.len(self.data.userStakePack[sp.sender][params[0]]) < params[1])
        amount = sp.nat(0)
        sp.if (self.data.userStakePack[sp.sender][params[0]][params[1]].timestamp.sp.add_days(self.data.Options[params[0]].stakingPeriod) > sp.now):
            amount = self.getReward(self.data.userStakePack[sp.sender][params[0]][params[1]], self.data.userStakePack[sp.sender][params[0]][params[1]].timestamp.sp.add_days(
                self.data.Options[params[0]].stakingPeriod)) + self.data.userStakePack[sp.sender][params[0]][params[1]].amount

        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, amount=amount)
        call(sp.contract(paramTrans, self.data.FA12TokenContract,entry_point="transfer").open_some(), paramCall)


    @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TNat)
        """ on vérifie que le sender a bien deja staké """
        sp.verify(self.data.userStakePack.contains(sp.sender))
        """ on vérifie que le sender a deja staké le pack qu'il veut redeem """
        sp.verify(self.data.userStakePack[sp.sender][0].contains(params))

        paramTrans = sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value")))
        paramCall = sp.record(from_=self.data.reserve, to_=sp.sender, amount=self.getReward(self.data.userStakePack[sp.sender][0][params], sp.now))
        call(sp.contract(paramTrans ,self.data.FA12TokenContract ,entry_point="transfer").open_some(), paramCall)
    """@sp.entry_point
    def unstakeAll(self):self.data.userstakePack[sp.sender][0]
        sp.verifiy(self.data.userstakePack.contains(sp.sender))
        sp.for i in sp.range(self.data.numPacks):
            sp.for j in sp.range(sp.len(self.data.userstakePack[sp.sender][i])):
                self.unstake(i, j, self.data.userstakePack[sp.sender][i][j].value)
    """

    def getReward(self, stake, end):
        k = sp.nat(10000)
        period = end - stake.timestamp
        timeRatio = (k * sp.as_nat(period) / sp.as_nat(sp.timestamp(1).add_days(365) - sp.timestamp(0)))
        reward = timeRatio * sp.as_nat(stake.rate)
        reward /= k
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
