# unipool-fork
A modified version of the [Synthetix](https://github.com/Synthetixio/synthetix) staking rewards contract, for use with [Curve.fi](https://github.com/curvefi) liquidity gauges.

## Overview

The [`StakingRewards`](contracts/StakingRewards.sol) contract in this repository is a flattened and modified version of the SNX [staking rewards](https://github.com/Synthetixio/synthetix/blob/master/contracts/StakingRewards.sol) contract.

The following modifications were made, to simplify integration with Curve's reward liquidity gauge:

1. The duration of the reward period is given as a constructor argument.

2. Transferring additional reward tokens into the contract is handled via `transferFrom`. This ensures the reward amount is always correct, and reduces the number of transactions required to fund the contract.

## Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) version 3.6 or greater, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.12.0](https://github.com/eth-brownie/brownie/releases/tag/v1.12.0)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.1)

## Usage

Prior to using these scripts you may wish to review the Brownie documentation on [Account management](https://eth-brownie.readthedocs.io/en/stable/account-management.html).

### Deployment

To deploy the contract, edit the constant variables at the top of [`scripts/deploy.py`](scripts/deploy.py). Then:

```bash
brownie run deploy --network mainnet
```

This script deploys [`StakingRewards`](contracts/StakingRewards.sol), set the initial reward period to one day, and seeds it with a single token. Once this is finished, please provide the Curve team with the deployment address so that we can verify the integration within our gauge.

### Updating Available Rewards

To update the available rewards, edit the constants at the top of [`scripts/update_rewards.py`](scripts/update_rewards.py). Then:

```bash
brownie run update_rewards --network mainnet
```

The exact functionality of the script is documented via the comments within it.

You must run this script, or otherwise complete the actions within it, at the start of each new reward period. As such, we recommend **30 days** as an optimal reward period duration.

## Testing

To validate the outcome of a script prior to running on mainnet, we recommend a dry-run in a forked mainnet environment:

```bash
brownie run update_rewards --network mainnet-fork -I
```

This command runs the script in a forked mainnet, and loads an interactive console upon completion. Within the console you can interact with the contracts to verify the expected outcome.

## Licence

The smart contract within this repository is forked from [Synthetixio/synthetix](https://github.com/Synthetixio/synthetix/tree/master) which is licensed under the [MIT license](https://github.com/Synthetixio/synthetix/blob/develop/LICENSE).

This repository is licensed under the [MIT license](LICENSE).
