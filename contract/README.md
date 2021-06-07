
# Originate the contract
As you can see, there are four directories inside. 
- **config**: required configuration in order to originate the contract
- **michelson-json**: smart contract and its storage in michelson json
- **origination**: script that originates the smart-contract
- **smartpy**: smart-contract in smartpy

While doing the operations, be sure to be in the `contract` directory.

## Originate a contract on the testnet
### Get a faucet account
1. Go to https://faucet.tzalpha.net/
2. Clic on "Get testnet" and testify that you're not a robot
3. Download the file

### Update the development configuration
1. Open the file called "development.env"
2. Replace the following information with the correspond information from your faucet file:
``` markdown
ADDRESS=
SIGNER_EMAIL=
SIGNER_PASSWORD=
SIGNER_MNEMONIC=
SIGNER_SECRET=
```
### Run the script
1. Export your dev environment variables:
``` bash
export NODE_ENV=development
```

2. Check that the env variable was set
``` bash
echo $NODE_ENV
```
It must output `development`. 

3. At the root of your project, run:
``` bash 
npm run originate
```

## Originate a contract on the mainnet
### Update the prod configuration
1. Go to the `config` directory
2. Create (or open if you already have one) your local file called `prod.env`
3. Add or update the required variables to your prod.env file
``` markdown
# environment
NODE_ENV=prod

########
# APIs #
########

RPC_ADDRESS=https://mainnet-tezos.giganode.io

#################################
# signer (smart contract owner) #
#################################

ADDRESS=
SIGNER_MNEMONIC=
SIGNER_SECRET=

############################
# smart contract variables #
############################

CONTRACT_FA12TOKEN_CONTRACT_ADDRESS=
CONTRACT_RESERVE_ADDRESS=
```
### Required libraries
Node 14 or higher is required to run the originate function. 

#### Install node on MAC
1. Go to https://nodejs.org/en/download/ and choose "macOS Installer".
2. Follow the instructions on the wizard. 
3. Once it is complete, to check that the installation was successful, run:

``` bash
node -v
npm -v
```

#### Install node on Linux
1. Open your terminal, and run:
``` bash
sudo apt update
sudo apt install nodejs npm
```

2. Once it is complete, to check that the installation was successful, run:

``` bash
node -v
npm -v
```

### Install dependencies
1. Check that you're in the right directory (`contract`)
``` bash
cd contract
```

2. To install the dependencies, run:
``` bash
npm install
```

### Let's originate the contract!
1. Export your prod environment variables:
``` bash
export NODE_ENV=prod
```

2. Check that the env variable was set
``` bash
echo $NODE_ENV
```
It must output `prod`. 

3. At the root of your project, run:
``` bash 
npm run originate
```
