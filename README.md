[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Discord][discord-shield]][discord-url]
[![Telegram][telegram-shield]][telegram-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]
[![Reddit][reddit-shield]][reddit-url]
![GitHub Logo](https://token.smartlink.so/wp-content/uploads/2021/04/Logo-HD-1.png)

# 1. Smartlink <a name="Smartlink"></a>
Smartlink addresses one of the biggest challenges in the global marketplace: ‘Need to Trust,’ by introducing decentralized escrow services and payments processing based on Tezos' institutional-grade smart contracts that suppress the need for buyers and sellers to trust each other.

Smartlink aims to provide a user-centered escrow solution to secure online and face-to-face transactions while broadening payments acceptance options through integrated wrapped currencies.

Smartlink proposes a new method to initiate commercial transactions by offering Trust-As-A-Service to incentivize commitment and eliminate the trust deficit in the global marketplace.

# 2. SMAK staking


    
- [1. Smartlink <a name="Smartlink"></a>](#1-smartlink-)
- [2. SMAK staking](#2-smak-staking)
  - [2.1. Variables <a name="Variables"></a>](#21-variables-)
    - [2.1.1. UserStakeLockPack <a name="UserStakeLockPack"></a>](#211-userstakelockpack-)
  - [2.2. Functions <a name="functions"></a>](#22-functions-)
    - [2.2.1. getters: <a name="getters"></a>](#221-getters-)
      - [2.2.1.1. getStakingOptions: <a name="getStakingOptions"></a>](#2211-getstakingoptions-)
      - [2.2.1.2. getStakingOptionById: <a name="getStakingOptionById"></a>](#2212-getstakingoptionbyid-)
      - [2.2.1.3. getAdmin: <a name="getReserve"></a>](#2213-getadmin-)
      - [2.2.1.4. getReserve: <a name="getReserve"></a>](#2214-getreserve-)
      - [2.2.1.5. getTokenContractAddress: <a name=""></a>](#2215-gettokencontractaddress-)
      - [2.2.1.6. getVotingContract: <a name="getVotingContract"></a>](#2216-getvotingcontract-)
      - [2.2.1.7. getAllStakeFlex: <a name="getAllStakeFlex"></a>](#2217-getallstakeflex-)
      - [2.2.1.8. getAllStakeLock: <a name="getAllStakeLock"></a>](#2218-getallstakelock-)
      - [2.2.1.9. getLockStakeByPack: <a name="getLockStakeByPack"></a>](#2219-getlockstakebypack-)
      - [2.2.1.10. getLockStakeInformation: <a name="getLockStakeInformation"></a>](#22110-getlockstakeinformation-)
      - [2.2.1.11. getLockStakeByPackAndId: <a name="getLockStakeByPackAndId"></a>](#22111-getlockstakebypackandid-)
      - [2.2.1.12. getFlexStakeInformation: <a name="getFlexStakeInformation"></a>](#22112-getflexstakeinformation-)
      - [2.2.1.13. getCurrentPendingRewards: <a name="getCurrentPendingRewards"></a>](#22113-getcurrentpendingrewards-)
    - [2.2.2. Setters](#222-setters)
      - [2.2.2.1. updateReserve: <a name="updateReserve"></a>](#2221-updatereserve-)
      - [2.2.2.2. updateAdmin: <a name="updateAdmin"></a>](#2222-updateadmin-)
      - [2.2.2.3. updateContract: <a name="updateContract"></a>](#2223-updatecontract-)
      - [2.2.2.4. updateVotingContract: <a name="updateVotingContract"></a>](#2224-updatevotingcontract-)
      - [2.2.2.5. is_voting_contract: <a name="is_voting_contract"></a>](#2225-is_voting_contract-)
      - [2.2.2.6. createStakingOption: <a name="createStakingOption"></a>](#2226-createstakingoption-)
      - [2.2.2.7. updateStakingOptionRate: <a name="updateStakingOptionRate"></a>](#2227-updatestakingoptionrate-)
      - [2.2.2.8. updateStakingOptionMax: <a name="updateStakingOptionMax"></a>](#2228-updatestakingoptionmax-)
      - [2.2.2.9. updateStakingOptionMin: <a name="updateStakingOptionMin"></a>](#2229-updatestakingoptionmin-)
    - [2.2.3. Core functions <a name="CoreFunc"></a>](#223-core-functions-)
      - [2.2.3.1. stakeLock: <a name=""></a>](#2231-stakelock-)
      - [2.2.3.2. stakeFlex: <a name="stakeFlex"></a>](#2232-stakeflex-)
      - [2.2.3.3. unstakeLock: <a name="unstakeLock"></a>](#2233-unstakelock-)
      - [2.2.3.4. unlockWithReward: <a name="unlockWithReward"></a>](#2234-unlockwithreward-)
      - [2.2.3.5. unlockWithoutReward: <a name="unlockWithoutReward"></a>](#2235-unlockwithoutreward-)
      - [2.2.3.6. unstakeFlex: <a name="unstakeFlex"></a>](#2236-unstakeflex-)
      - [2.2.3.7. claimRewardFlex: <a name="claimRewardFlex"></a>](#2237-claimrewardflex-)
      - [2.2.3.8. getReward: <a name="getReward"></a>](#2238-getreward-)

## 2.1. Variables <a name="Variables"></a>
| Name                              |      Type                                |                     Description                                                                                                                        |
|----------------------------------:|:----------------------------------------:|:---------------------------------------------------------------------------|
| admin                             |         TAddress                         |Address of the admin                                                        |
| reserve                           |          TAddress                        |Address of the token reserve to pay the stakings                            |
|userStakeLockPack                  |[UserStakeLockPack](#UserStakeLockPack)   |See the schema below                                                        |
| StakeLock                         |        TRecord                           |Structure of a staking locked                                               |
| StakeLock.timestamp               |        TTimestamp                        |Timestamp of the begining of the staking                                    |
| StakeLock.rate                    |        TNat                              |Rate of the staking                                                         |
| StakeLock.value                   |        TNat                              |Amount of tokens staked                                                     |
| userStakeFlexPack                 |   TBig_map(TAddress, StakeFlex)          |Storage of all the flex stakings                                            |
| StakeFlex                         |        TRecord                           |Structure of a staking flex                                                 |
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

### 2.1.1. UserStakeLockPack <a name="UserStakeLockPack"></a>
This is the structure of the nested maps ```userStakeLockPack```
<img src="https://ipfs.io/ipfs/QmYsv8WVrQd1pX2KRQCjLT1N27abQtstxuy6Ct1qxbmfto" alt="UserStakeLockPack's structure">

## 2.2. Functions <a name="functions"></a>
### 2.2.1. getters: <a name="getters"></a>
#### 2.2.1.1. getStakingOptions: <a name="getStakingOptions"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat)))
    def getStakingOptions(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map if staking options

#### 2.2.1.2. getStakingOptionById: <a name="getStakingOptionById"></a>
```python
@sp.utils.view(sp.TRecord(minStake=sp.TNat, maxStake=sp.TNat, stakingPeriod=sp.TInt, stakingPercentage=sp.TNat))
    def getStakingOptionById(self, params):
        sp.set_type(params, sp.TNat)
```
Returns the specified staking option

#### 2.2.1.3. getAdmin: <a name="getReserve"></a>
```python
@sp.utils.view(sp.TAddress)
    def getAdmin(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the admin

#### 2.2.1.4. getReserve: <a name="getReserve"></a>
```python
@sp.utils.view(sp.TAddress)
    def getReserve(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the reserve which will pay the staking rewards

#### 2.2.1.5. getTokenContractAddress: <a name=""></a>
```python
@sp.utils.view(sp.TAddress)
    def getTokenContractAddress(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the token contract

#### 2.2.1.6. getVotingContract: <a name="getVotingContract"></a>
```python
 @sp.utils.view(sp.TAddress)
    def getVotingContract(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the address of the voting contract

#### 2.2.1.7. getAllStakeFlex: <a name="getAllStakeFlex"></a>
```python
@sp.utils.view(sp.TBigMap(sp.TAddress, StakeFlex))
    def getAllStakeFlex(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map of the flex stakings

#### 2.2.1.8. getAllStakeLock: <a name="getAllStakeLock"></a>
```python
@sp.utils.view(sp.TBigMap(sp.TAddress, sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock))))
    def getAllStakeLock(self, params):
        sp.set_type(params, sp.TUnit)
```
Returns the whole map of locked stakings

#### 2.2.1.9. getLockStakeByPack: <a name="getLockStakeByPack"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, StakeLock))
    def getLockStakeByPack(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, address = sp.TAddress))
```
Returns all the stakings of a specified user for a specified pack

#### 2.2.1.10. getLockStakeInformation: <a name="getLockStakeInformation"></a>
```python
@sp.utils.view(sp.TMap(sp.TNat, sp.TMap(sp.TNat, StakeLock)))
    def getLockStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns all the locked stakings for a specified user

#### 2.2.1.11. getLockStakeByPackAndId: <a name="getLockStakeByPackAndId"></a>
```python
@sp.utils.view(StakeLock)
    def getLockStakeByPackAndId(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, address = sp.TAddress, id_ = sp.TNat).layout(("id_ as id", ("pack", "address"))))
```
Returns the specified staking

#### 2.2.1.12. getFlexStakeInformation: <a name="getFlexStakeInformation"></a>
```python
@sp.utils.view(StakeFlex)
    def getFlexStakeInformation(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns the flex staking of the specified user

#### 2.2.1.13. getCurrentPendingRewards: <a name="getCurrentPendingRewards"></a>
```python
@sp.utils.view(sp.TNat)
    def getCurrentPendingRewards(self, params):
        sp.set_type(params, sp.TAddress)
```
Returns the pending rewards for a user

### 2.2.2. Setters
#### 2.2.2.1. updateReserve: <a name="updateReserve"></a>
```python
@sp.entry_point
    def updateReserve(self, params):
        sp.set_type(params, sp.TRecord(reserve=sp.TAddress))
```
Sets the reserve address
#### 2.2.2.2. updateAdmin: <a name="updateAdmin"></a>
```python
 @sp.entry_point
    def updateAdmin(self, params):
        sp.set_type(params, sp.TRecord(admin=sp.TAddress))
```
Set the admin address of the contract
#### 2.2.2.3. updateContract: <a name="updateContract"></a>
```python
@sp.entry_point
    def updateContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
```
Set the address of the token contract
#### 2.2.2.4. updateVotingContract: <a name="updateVotingContract"></a>
```python
@sp.entry_point
    def updateVotingContract(self, params):
        sp.set_type(params, sp.TRecord(contract = sp.TAddress))
```
Set the adress of the voting contract
#### 2.2.2.5. is_voting_contract: <a name="is_voting_contract"></a>
```python
@sp.sub_entry_point
    def is_voting_contract(self, contract):
```
Verify if the address in param is the voting contract address
#### 2.2.2.6. createStakingOption: <a name="createStakingOption"></a>
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
#### 2.2.2.7. updateStakingOptionRate: <a name="updateStakingOptionRate"></a>
```python
@sp.entry_point
    def updateStakingOptionRate(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, rate = sp.TNat).layout(("_id as id", "rate")))
```
Function used to set the new duration of the staking pack
#### 2.2.2.8. updateStakingOptionMax: <a name="updateStakingOptionMax"></a>
```python
   @sp.entry_point
    def updateStakingOptionMax(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _max = sp.TNat).layout(("_id as id", "_max as max")))
```
Function used to set the new max amount per transaction
#### 2.2.2.9. updateStakingOptionMin: <a name="updateStakingOptionMin"></a>
```python
@sp.entry_point
    def updateStakingOptionMin(self, params):
        sp.set_type(params, sp.TRecord(_id = sp.TNat, _min = sp.TNat).layout(("_id as id", "_min as min")))
```
Function used to set the new min per transaction 

### 2.2.3. Core functions <a name="CoreFunc"></a>
#### 2.2.3.1. stakeLock: <a name=""></a>
```python
 @sp.entry_point
    def stakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, amount = sp.TNat))
```
Stakes the amount of tokens with using the parameters of the pack specified. Will initialize the map for the user if it's his first staking

#### 2.2.3.2. stakeFlex: <a name="stakeFlex"></a>
```python
@sp.entry_point
    def stakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
```
Stakes the amount of tokens using the flex pack parameters. Will initialize the staking for the user if it's his first staking. Else it will only update the staking

#### 2.2.3.3. unstakeLock: <a name="unstakeLock"></a>
```python
@sp.entry_point
    def unstakeLock(self, params):
        sp.set_type(params, sp.TRecord(pack=sp.TNat, index=sp.TNat))
```
Unstakes the specified stake. If the stake period isn't finished the user won't receive his rewards.

#### 2.2.3.4. unlockWithReward: <a name="unlockWithReward"></a>
```python
@sp.sub_entry_point
    def unlockWithReward(self, params):
        sp.set_type(params, sp.TRecord(pack = sp.TNat, index = sp.TNat))
```
Function called by ```unstakeLock``` if the staking period has finished. Will send the user his tokens back + the rewards

#### 2.2.3.5. unlockWithoutReward: <a name="unlockWithoutReward"></a>
```python
 @sp.sub_entry_point
    def unlockWithoutReward(self, params):
        sp.set_type(params, sp.TRecord(index = sp.TNat, pack = sp.TNat))
```
Function called by ```unstakeLock``` if the staking period has not finished. Will only send the user his tokens back.

#### 2.2.3.6. unstakeFlex: <a name="unstakeFlex"></a>
```python
 @sp.entry_point
    def unstakeFlex(self, params):
        sp.set_type(params, sp.TRecord(amount = sp.TNat))
```
Computes the reward for the last staking period, sets the timestamp to the actual timestamp, updates the value of the stake and sends the user his tokens back.

#### 2.2.3.7. claimRewardFlex: <a name="claimRewardFlex"></a>
```python
@sp.entry_point
    def claimRewardFlex(self):
```
Sends the rewards available to the user

#### 2.2.3.8. getReward: <a name="getReward"></a>
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

- [1. Smartlink <a name="Smartlink"></a>](#1-smartlink-)
- [2. SMAK staking](#2-smak-staking)
  - [2.1. Variables <a name="Variables"></a>](#21-variables-)
    - [2.1.1. UserStakeLockPack <a name="UserStakeLockPack"></a>](#211-userstakelockpack-)
  - [2.2. Functions <a name="functions"></a>](#22-functions-)
    - [2.2.1. getters: <a name="getters"></a>](#221-getters-)
      - [2.2.1.1. getStakingOptions: <a name="getStakingOptions"></a>](#2211-getstakingoptions-)
      - [2.2.1.2. getStakingOptionById: <a name="getStakingOptionById"></a>](#2212-getstakingoptionbyid-)
      - [2.2.1.3. getAdmin: <a name="getReserve"></a>](#2213-getadmin-)
      - [2.2.1.4. getReserve: <a name="getReserve"></a>](#2214-getreserve-)
      - [2.2.1.5. getTokenContractAddress: <a name=""></a>](#2215-gettokencontractaddress-)
      - [2.2.1.6. getVotingContract: <a name="getVotingContract"></a>](#2216-getvotingcontract-)
      - [2.2.1.7. getAllStakeFlex: <a name="getAllStakeFlex"></a>](#2217-getallstakeflex-)
      - [2.2.1.8. getAllStakeLock: <a name="getAllStakeLock"></a>](#2218-getallstakelock-)
      - [2.2.1.9. getLockStakeByPack: <a name="getLockStakeByPack"></a>](#2219-getlockstakebypack-)
      - [2.2.1.10. getLockStakeInformation: <a name="getLockStakeInformation"></a>](#22110-getlockstakeinformation-)
      - [2.2.1.11. getLockStakeByPackAndId: <a name="getLockStakeByPackAndId"></a>](#22111-getlockstakebypackandid-)
      - [2.2.1.12. getFlexStakeInformation: <a name="getFlexStakeInformation"></a>](#22112-getflexstakeinformation-)
      - [2.2.1.13. getCurrentPendingRewards: <a name="getCurrentPendingRewards"></a>](#22113-getcurrentpendingrewards-)
    - [2.2.2. Setters](#222-setters)
      - [2.2.2.1. updateReserve: <a name="updateReserve"></a>](#2221-updatereserve-)
      - [2.2.2.2. updateAdmin: <a name="updateAdmin"></a>](#2222-updateadmin-)
      - [2.2.2.3. updateContract: <a name="updateContract"></a>](#2223-updatecontract-)
      - [2.2.2.4. updateVotingContract: <a name="updateVotingContract"></a>](#2224-updatevotingcontract-)
      - [2.2.2.5. is_voting_contract: <a name="is_voting_contract"></a>](#2225-is_voting_contract-)
      - [2.2.2.6. createStakingOption: <a name="createStakingOption"></a>](#2226-createstakingoption-)
      - [2.2.2.7. updateStakingOptionRate: <a name="updateStakingOptionRate"></a>](#2227-updatestakingoptionrate-)
      - [2.2.2.8. updateStakingOptionMax: <a name="updateStakingOptionMax"></a>](#2228-updatestakingoptionmax-)
      - [2.2.2.9. updateStakingOptionMin: <a name="updateStakingOptionMin"></a>](#2229-updatestakingoptionmin-)
    - [2.2.3. Core functions <a name="CoreFunc"></a>](#223-core-functions-)
      - [2.2.3.1. stakeLock: <a name=""></a>](#2231-stakelock-)
      - [2.2.3.2. stakeFlex: <a name="stakeFlex"></a>](#2232-stakeflex-)
      - [2.2.3.3. unstakeLock: <a name="unstakeLock"></a>](#2233-unstakelock-)
      - [2.2.3.4. unlockWithReward: <a name="unlockWithReward"></a>](#2234-unlockwithreward-)
      - [2.2.3.5. unlockWithoutReward: <a name="unlockWithoutReward"></a>](#2235-unlockwithoutreward-)
      - [2.2.3.6. unstakeFlex: <a name="unstakeFlex"></a>](#2236-unstakeflex-)
      - [2.2.3.7. claimRewardFlex: <a name="claimRewardFlex"></a>](#2237-claimrewardflex-)
      - [2.2.3.8. getReward: <a name="getReward"></a>](#2238-getreward-)
