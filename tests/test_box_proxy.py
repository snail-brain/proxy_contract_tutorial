from weakref import proxy
from scripts.helpful_scripts import *
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    account = getAccount()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_init_func = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_init_func,
        {"from": account, "gas": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
