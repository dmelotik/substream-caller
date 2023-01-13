# Substream Caller

WIP: Use https://github.com/messari/substreams-python instead :)

This python script will call substream modules from https://github.com/messari/substreams and store up the results.

## Setup

Setup your substream environment variables. See: https://substreams.streamingfast.io/getting-started/quickstart#authentication

Build an `spkg` file for your substream module, and place it in `./spkgs/`.

To build an spkg:

```bash
substreams pack ./substreams.yaml
```

Install some shit:
```bash
pip3 install grpcio-tools protobuf==3.20.1
```

To run the caller:
```bash
python3 main.py --spkg erc20-contracts --start 1 --next 100 --module map_block_to_erc20_contracts

python3 main.py --spkg erc20-contracts --start 565000 --next 15830 --module map_block_to_erc20_contracts
```

`--spkg`: your substream module name without the path or file descriptor

`--start`: the starting block number

`--next`: the number of blocks to process

`--module`: the name of the module to call
