from scripts.helpful_scripts import *
from brownie import (
    Box,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    Contract,
    BoxV2,
    exceptions,
)
import pytest


def test_upgrade():
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

    box2 = BoxV2.deploy({"from": account})
    proxy_box2 = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box2.increment({"from": account})
    upgrade(account, proxy, box2.address, proxy_admin)

    proxy_box2.store(1, {"from": account})

    assert proxy_box2.retrieve() == 1

    proxy_box2.increment({"from": account})

    assert proxy_box2.retrieve() == 2
