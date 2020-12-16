from brownie import Contract, StakingRewards, accounts
from brownie.network.gas.strategies import GasNowScalingStrategy


# the address that will be used to deploy the contract
# can be loaded via a keystore or private key, for more info see
# https://eth-brownie.readthedocs.io/en/stable/account-management.html
DEPLOYER = accounts.add()
# the address that owns the contract and can call all restricted functions
OWNER = DEPLOYER
# the address that is permitted to fund the contract
REWARD_ADMIN = DEPLOYER

# the address of the token you will be giving as a staking reward
REWARD_TOKEN_ADDRESS = "0x"
# the address of the Curve LP token for your pool
STAKING_TOKEN_ADDRESS = "0x"


gas_strategy = GasNowScalingStrategy("standard", "fast")


def main():
    token = Contract(REWARD_TOKEN_ADDRESS)
    seed_amount = 10 ** token.decimals()
    if token.balanceOf(REWARD_ADMIN) < seed_amount:
        raise ValueError("Reward admin must have at least 1 token to seed the contract for testing")

    # deploy the rewards contract - initially we set the reward period to one day so we
    # can seed a small amount for testing
    rewards = StakingRewards.deploy(
        OWNER,
        REWARD_ADMIN,
        token,
        STAKING_TOKEN_ADDRESS,
        86400,
        {'from': DEPLOYER, 'gas_price': gas_strategy}
    )

    # give infinite approval to the reward contract from the reward admin
    token.approve(rewards, 2**256-1, {'from': REWARD_ADMIN, 'gas_price': gas_strategy})

    # seed the contract with 1 token for initial testing
    rewards.notifyRewardAmount(seed_amount, {'from': REWARD_ADMIN, 'gas_price': gas_strategy})

    print(f"""Success!

StakingRewards deployed to: {rewards}
Owner: {OWNER}
Reward admin: {REWARD_ADMIN}

Please verify the source code on Etherscan here: https://etherscan.io/verifyContract?a={rewards}
Compiler version: 0.5.17
Optimization: ON
""")
