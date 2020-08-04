from tronpy import Tron, Contract
from tronpy.keys import PrivateKey


def test_const_functions():
    client = Tron(network='nile')

    contract = client.get_contract('THi2qJf6XmvTJSpZHc17HgQsmJop6kb3ia')
    assert contract

    assert 'name' in dir(contract.functions)

    print(dir(contract.functions))
    print(repr(contract.functions.name()))
    print(repr(contract.functions.decimals()))

    assert contract.functions.totalSupply() > 0

    for f in contract.functions:
        print(f)


def test_trc20_transfer():
    # TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu
    priv_key = PrivateKey(bytes.fromhex("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"))

    client = Tron(network='nile')

    contract = client.get_contract('THi2qJf6XmvTJSpZHc17HgQsmJop6kb3ia')
    print('Balance', contract.functions.balanceOf('TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu'))
    txn = (
        contract.functions.transfer('TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA', 1_000)
        .with_owner('TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu')
        .fee_limit(1_000_000)
        .build()
        .sign(priv_key)
        .inspect()
        .broadcast()
    )

    print(txn)
    # wait
    receipt = txn.wait()
    print(receipt)
    if 'contractResult' in receipt:
        print('result:', contract.functions.transfer.parse_output(receipt['contractResult'][0]))

    # result
    print(txn.result())


def test_contract_create():
    # TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu
    priv_key = PrivateKey(bytes.fromhex("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"))
    client = Tron(network='nile')

    bytecode = "608060405234801561001057600080fd5b5060c78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c806360fe47b11460375780636d4ce63c146062575b600080fd5b606060048036036020811015604b57600080fd5b8101908080359060200190929190505050607e565b005b60686088565b6040518082815260200191505060405180910390f35b8060008190555050565b6000805490509056fea2646970667358221220c8daade51f673e96205b4a991ab6b94af82edea0f4b57be087ab123f03fc40f264736f6c63430006000033"
    abi = [
        {
            "inputs": [],
            "name": "get",
            "outputs": [{"internalType": "uint256", "name": "retVal", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        }
    ]

    cntr = Contract(name="SimpleStore", bytecode=bytecode, abi=abi)

    # https://developers.tron.network/docs/setting-a-fee-limit-on-deployexecution
    # The maximum limit is 1000 TRX, or 1e9 SUN. Setting it to a value larger than 1e9 will produce an error.
    # When deploying large contracts or running complex functions, this limit may need to be increased up to 1000 TRX. However, check out timeouts, infinite loops, illegal operations, and non-existent account transfer sections are why setting a higher limit may sometimes be bad practice.

    # The maximum limit is 1000 TRX, or 1e9 SUN. Setting it to a value larger than 1e9 will produce an error.
    # feeLimit: 1e9,  // Set fee limit

    txn = (
        client.trx.deploy_contract('TGQgfK497YXmjdgvun9Bg5Zu3xE15v17cu', cntr)
        .fee_limit(1000000000)
        .build()
        .sign(priv_key)
        .inspect()
        .broadcast()
    )
    print(txn)
    result = txn.wait()
    print(result)
    print('Created:', result['contract_address'])
