import datetime

from brownie import Contract, StakingRewards, accounts, chain
from brownie.network.gas.strategies import GasNowScalingStrategy


# address of the StakingRewards contract
REWARDS_CONTRACT_ADDRESS = "0x"

# address that owns `StakingRewards`
OWNER = accounts.add()
# address that is permitted to fund the contract
REWARD_ADMIN = OWNER

# amount to add as a reward
REWARDS_AMOUNT = 0
# duration of the rewards period, in seconds - we recommend keeping this as 30 days
REWARDS_DURATION = 30 * 86400


gas_strategy = GasNowScalingStrategy("standard", "fast")


def main():
    rewards = StakingRewards.at(REWARDS_CONTRACT_ADDRESS)
    token = Contract(rewards.rewardsToken())

    # sanity check on the reward amount
    if REWARDS_AMOUNT < 10 ** token.decimals():
        raise ValueError("Reward amount is less than 1 token - are you sure this is correct?")

    # ensure the reward admin has sufficient balance of the reward token
    if token.balanceOf(REWARD_ADMIN) < REWARDS_AMOUNT:
        raise ValueError("Rewards admin has insufficient balance to fund the contract")

    # check the reward duration and modify if needed
    if rewards.rewardsDuration() != REWARDS_DURATION:
        remaining_time = rewards.periodFinish() - chain[-1].timestamp
        if remaining_time > 0:
            raise ValueError(
                "Current reward period must finish before the period duration can be modified, "
                f"try again in {datetime.timedelta(seconds=remaining_time)}"
            )
        rewards.setRewardsDuration(REWARDS_DURATION, {'from': OWNER})

    # ensure the reward contract has sufficient allowance to transfer the reward token
    if token.allowance(REWARD_ADMIN, rewards) < REWARDS_AMOUNT:
        token.approve(rewards, 2**256-1, {'from': REWARD_ADMIN, 'gas_price': gas_strategy})

    # update the reward amount
    rewards.notifyRewardAmount(REWARDS_AMOUNT, {'from': REWARD_ADMIN, 'gas_price': gas_strategy})

    print(
        f"Success! {REWARDS_AMOUNT/10**token.decimals():.2f} {token.symbol()} has been added to "
        f"the rewards contract, to be distributed over {REWARDS_DURATION/86400:.1f} days."
    )
