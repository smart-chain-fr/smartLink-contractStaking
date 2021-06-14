[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Discord][discord-shield]][discord-url]
[![Telegram][telegram-shield]][telegram-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]
[![Reddit][reddit-shield]][reddit-url]
![GitHub Logo](https://token.smartlink.so/wp-content/uploads/2021/04/Logo-HD-1.png)

# Smartlink <a name="Smartlink"></a>
Smartlink addresses one of the biggest challenges in the global marketplace: ‘Need to Trust,’ by introducing decentralized escrow services and payments processing based on Tezos' institutional-grade smart contracts that suppress the need for buyers and sellers to trust each other.

Smartlink aims to provide a user-centered escrow solution to secure online and face-to-face transactions while broadening payments acceptance options through integrated wrapped currencies.

Smartlink proposes a new method to initiate commercial transactions by offering Trust-As-A-Service to incentivize commitment and eliminate the trust deficit in the global marketplace.

# SMAK staking


    
- [Smartlink <a name="Smartlink"></a>](#smartlink-)
- [SMAK staking](#smak-staking)
  - [Variables <a name="Variables"></a>](#variables-)
    - [UserStakeLockPack <a name="UserStakeLockPack"></a>](#userstakelockpack-)
  - [Functions <a name="functions"></a>](#functions-)
    - [getters: <a name="getters"></a>](#getters-)
      - [getStakingOptions: <a name="getStakingOptions"></a>](#getstakingoptions-)
      - [getStakingOptionById: <a name="getStakingOptionById"></a>](#getstakingoptionbyid-)
      - [getAdmin: <a name="getReserve"></a>](#getadmin-)
      - [getReserve: <a name="getReserve"></a>](#getreserve-)
      - [getTokenContractAddress: <a name=""></a>](#gettokencontractaddress-)
      - [getVotingContract: <a name="getVotingContract"></a>](#getvotingcontract-)
      - [getAllStakeFlex: <a name="getAllStakeFlex"></a>](#getallstakeflex-)
      - [getAllStakeLock: <a name="getAllStakeLock"></a>](#getallstakelock-)
      - [getLockStakeByPack: <a name="getLockStakeByPack"></a>](#getlockstakebypack-)
      - [getLockStakeInformation: <a name="getLockStakeInformation"></a>](#getlockstakeinformation-)
      - [getLockStakeByPackAndId: <a name="getLockStakeByPackAndId"></a>](#getlockstakebypackandid-)
      - [getFlexStakeInformation: <a name="getFlexStakeInformation"></a>](#getflexstakeinformation-)
      - [getCurrentPendingRewards: <a name="getCurrentPendingRewards"></a>](#getcurrentpendingrewards-)
    - [Setters](#setters)
      - [updateReserve: <a name="updateReserve"></a>](#updatereserve-)
      - [updateAdmin: <a name="updateAdmin"></a>](#updateadmin-)
      - [updateContract: <a name="updateContract"></a>](#updatecontract-)
      - [updateVotingContract: <a name="updateVotingContract"></a>](#updatevotingcontract-)
      - [is_voting_contract: <a name="is_voting_contract"></a>](#is_voting_contract-)
      - [createStakingOption: <a name="createStakingOption"></a>](#createstakingoption-)
      - [updateStakingOptionRate: <a name="updateStakingOptionRate"></a>](#updatestakingoptionrate-)
      - [updateStakingOptionMax: <a name="updateStakingOptionMax"></a>](#updatestakingoptionmax-)
      - [updateStakingOptionMin: <a name="updateStakingOptionMin"></a>](#updatestakingoptionmin-)
    - [Core functions <a name="CoreFunc"></a>](#core-functions-)
      - [stakeLock: <a name=""></a>](#stakelock-)
      - [stakeFlex: <a name="stakeFlex"></a>](#stakeflex-)
      - [unstakeLock: <a name="unstakeLock"></a>](#unstakelock-)
      - [unlockWithReward: <a name="unlockWithReward"></a>](#unlockwithreward-)
      - [unlockWithoutReward: <a name="unlockWithoutReward"></a>](#unlockwithoutreward-)
      - [unstakeFlex: <a name="unstakeFlex"></a>](#unstakeflex-)
      - [claimRewardFlex: <a name="claimRewardFlex"></a>](#claimrewardflex-)
      - [getReward: <a name="getReward"></a>](#getreward-)

## Variables <a name="Variables"></a>
| Name                              |      Type                                |                     Description                                                                                                                        |
|----------------------------------:|:----------------------------------------:|:---------------------------------------------------------------------------|
| admin                             |         TAddress                         |Address of the admin                                                        |
| reserve                           |          TAddress                        |Address of the token reserve to pay the stakings                            |
|userStakeLockPack                  |[UserStakeLockPack](#UserStakeLockPack)   |See the schema below                                                        |
| StakeLock                         |        TRecord                           |Structure of a locked staking                                               |
| StakeLock.timestamp               |        TTimestamp                        |Timestamp of the begining of the staking                                    |
| StakeLock.rate                    |        TNat                              |Rate of the staking                                                         |
| StakeLock.value                   |        TNat                              |Amount of tokens staked                                                     |
| userStakeFlexPack                 |   TBig_map(TAddress, StakeFlex)          |Storage of all the flex stakings                                            |
| StakeFlex                         |        TRecord                           |Structure of a flex staking                                                 |
| StakeFlex.timestamp               |        TTimestamp                        |Timestamp of the begining of the staking                                    |
| StakeLock.reward                  |        TNat                              |Rewards for the past period of the staking                                  |
| StakeLock.value                   |        TNat                              |Amount of tokens staked                                                     |
| stakingOptions                    |           TMap(TNat, stakingOption)      |Storage of all the staking packs                                            |
| stakingOption                     |        TRecord                           |Structure of a staking option                                               |
| stakingOption.minStake            |        TNat                              |Minimum amount of tokens that can be sent in one transaction                |                     |
| stakingOption.maxStake            |        TNat                              |Maximum amount of tokens that can be sent in one transaction                |                      |
| stakingOption.stakingPeriod       |        TInt                              |Duration of a staking                                                       |
| stakingOption.stakingPercentage   |        TNat                              |Rate of the staking                                                         |
| votingContract                    |         TAddress                         |Address of the voting contract that will be implemented in the future       |                                                     |
| stakingHistory                    |TMap(TTimestamp, TInt)                    |Mapping of the number of SMAK staked at a timestamp                         |

### UserStakeLockPack <a name="UserStakeLockPack"></a>
This is the structure of the nested maps ```userStakeLockPack```
<img src="https://ipfs.io/ipfs/QmYsv8WVrQd1pX2KRQCjLT1N27abQtstxuy6Ct1qxbmfto" alt="UserStakeLockPack's structure">

## Functions <a name="functions"></a>
### getters: <a name="getters"></a>
#### getStakingOptions: <a name="getStakingOptions"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat)))
    def getStakingOptions(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map of staking options

#### getStakingOptionById: <a name="getStakingOptionById"></a>
```python
@sp.utils.view(sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat))
    def getStakingOptionById(self, params):
        sp.set_type(params, sp.TNat)
```
Returns the specified staking option

#### getAdmin: <a name="getReserve"></a>
```python
@sp.utils.view(sp.TAddress)
    def getAdmin(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the admin

#### getReserve: <a name="getReserve"></a>
```python
@sp.utils.view(sp.TAddress)
    def getReserve(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the reserve which will pay the staking rewards

#### getTokenContractAddress: <a name=""></a>
```python
@sp.utils.view(sp.TAddress)
    def getTokenContractAddress(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the token contract

#### getVotingContract: <a name="getVotingContract"></a>
```python
 @sp.utils.view(sp.TAddress)
    def getVotingContract(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the voting contract

#### getAllStakeFlex: <a name="getAllStakeFlex"></a>
```python
@sp.utils.view(sp.TBigMap(sp.TAddress, StakeFlex))
    def getAllStakeFlex(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map of the flex stakings

#### getAllStakeLock: <a name="getAllStakeLock"></a>
```python
@sp.utils.view(sp.TBigMap(sp.TAddress, sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock))))
    def getAllStakeLock(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map of locked stakings

#### getLockStakeByPack: <a name="getLockStakeByPack"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, StakeLock))
    def getLockStakeByPack(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, address = sp.TAddress))
```
Returns all the stakings of a specified user for a specified pack

#### getLockStakeInformation: <a name="getLockStakeInformation"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock)))
    def getLockStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns all the locked stakings for a specified user

#### getLockStakeByPackAndId: <a name="getLockStakeByPackAndId"></a>
```python
@sp.utils.view(StakeLock)
    def getLockStakeByPackAndId(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, address = sp.TAddress, id_ = sp.TNat).layout(("id_ as id", ("pack", "address"))))
```
Returns a specified staking of a specified pack of a specified user

#### getFlexStakeInformation: <a name="getFlexStakeInformation"></a>
```python
@sp.utils.view(StakeFlex)
    def getFlexStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns the flex staking of the specified user

#### getCurrentPendingRewards: <a name="getCurrentPendingRewards"></a>
```python
@sp.utils.view(sp.TNat)
    def getCurrentPendingRewards(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns the pending rewards for a user

### Setters
#### updateReserve: <a name="updateReserve"></a>
```python
@sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve=sp.TAddress))
```
Sets the reserve address

#### updateAdmin: <a name="updateAdmin"></a>
```python
 @sp.entry_point
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin=sp.TAddress))
```
Sets the admin address of the contract

#### updateContract: <a name="updateContract"></a>
```python
@sp.entry_point
    def updateContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
```
Sets the address of the token contract

#### updateVotingContract: <a name="updateVotingContract"></a>
```python
@sp.entry_point
    def updateVotingContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
```
Sets the adress of the voting contract

#### is_voting_contract: <a name="is_voting_contract"></a>
```python
@sp.sub_entry_point
    def is_voting_contract(self, contract):
```
Verifies if the address in param is the voting contract address

#### createStakingOption: <a name="createStakingOption"></a>
```python
 @sp.entry_point
    def createStakingOption(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat, _max = sp.TNat, _min = sp.TNat, duration = sp.TInt).layout(("_id as id", ("rate", ("_max as max", ("_min as min", "duration"))))))
```
Function used to create a stacking pack (Period / APY). Only Admin 
- the id of the staking parameters
- the staking rate
- the maximum staking amount per transaction
- the minimum staking amount per transaction
- the staking period
#### updateStakingOptionRate: <a name="updateStakingOptionRate"></a>
```python
@sp.entry_point
    def updateStakingOptionRate(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat).layout(("_id as id", "rate")))
```
Sets the new duration of the staking pack

#### updateStakingOptionMax: <a name="updateStakingOptionMax"></a>
```python
   @sp.entry_point
    def updateStakingOptionMax(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _max = sp.TNat).layout(("_id as id", "_max as max")))
```
Sets the new max amount per transaction

#### updateStakingOptionMin: <a name="updateStakingOptionMin"></a>
```python
@sp.entry_point
    def updateStakingOptionMin(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _min = sp.TNat).layout(("_id as id", "_min as min")))
```
Sets the new min per transaction 

### Core functions <a name="CoreFunc"></a>
#### stakeLock: <a name=""></a>
```python
 @sp.entry_point
    def stakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, amount = sp.TNat))
```
Stakes the amount of tokens using the parameters of the pack specified. Will initialize the map for the user if it's his first staking

#### stakeFlex: <a name="stakeFlex"></a>
```python
@sp.entry_point
    def stakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
```
Stakes the amount of tokens using the flex pack parameters. Will initialize the staking for the user if it's his first staking. Else it will only update the staking

#### unstakeLock: <a name="unstakeLock"></a>
```python
@sp.entry_point
    def unstakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack=sp.TNat, index=sp.TNat))
```
Unstakes the specified stake. If the stake period isn't finished the user won't receive his rewards.

#### unlockWithReward: <a name="unlockWithReward"></a>
```python
@sp.sub_entry_point
    def unlockWithReward(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, index = sp.TNat))
```
Function called by ```unstakeLock``` if the staking period has finished. Will send the user his tokens back + the rewards

#### unlockWithoutReward: <a name="unlockWithoutReward"></a>
```python
 @sp.sub_entry_point
    def unlockWithoutReward(self, params):
        sp.set_type(params, sp.TRecord(index = sp.TNat, pack = sp.TNat))
```
Function called by ```unstakeLock``` if the staking period has not finished. Will only send the user his tokens back.

#### unstakeFlex: <a name="unstakeFlex"></a>
```python
 @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
```
Computes the reward for the last staking period, sets the timestamp to the actual timestamp, updates the value of the stake and sends the user his tokens back.

#### claimRewardFlex: <a name="claimRewardFlex"></a>
```python
@sp.entry_point
    def claimRewardFlex(self):
```
Sends the rewards available to the user

#### getReward: <a name="getReward"></a>
```python
 def getReward(self, params):
        sp.set_type(params, sp.TRecord(start=sp.TTimestamp, end = sp.TTimestamp, value= sp.TNat, rate=sp.TNat))
```
Internal function that will compute the rewards for a period



[contributors-shield]: https://img.shields.io/github/contributors/Smartlinkhub/SMAK-Staking.svg?style=for-the-badge
[contributors-url]: https://github.com/Smartlinkhub/SMAK-Staking/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Smartlinkhub/SMAK-Staking.svg?style=for-the-badge
[forks-url]: https://github.com/Smartlinkhub/SMAK-Staking/network/members
[telegram-url]: https://t.me/smartlinkofficial
[telegram-shield]: https://img.shields.io/badge/-Telegram-black.svg?style=for-the-badge&logo=Telegram&colorB=555
[linkedin-url]: https://www.linkedin.com/company/smartlinkso
[linkedin-shield]: https://img.shields.io/badge/-Linkedin-black.svg?style=for-the-badge&logo=Linkedin&colorB=555
[discord-shield]: https://img.shields.io/badge/-Discord-black.svg?style=for-the-badge&logo=discord&colorB=555
[discord-url]:https://discord.gg/Rut5xxqGWQ
[twitter-shield]: https://img.shields.io/badge/-Twitter-black.svg?style=for-the-badge&logo=twitter&colorB=555
[twitter-url]:https://twitter.com/smartlinkHQ
[reddit-shield]: https://img.shields.io/badge/-reddit-black.svg?style=for-the-badge&logo=reddit&colorB=555
[reddit-url]:https://www.reddit.com/user/Teamsmartlink/

