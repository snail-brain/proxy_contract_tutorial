from weakref import proxy
from scripts.helpful_scripts import *
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():

    # Deploy the Implementation Contract
    account = getAccount()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})

    # Deploy Proxy Admin Contract
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # If we were to have an initializer, we would encode the parameter data and pass it to the proxy contract
    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    # Deploy Proxy Contract
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas": 1000000},
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2!")

    # Interact with implementation contract through our proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    # Deploy upgrade to implementation contract
    box2 = BoxV2.deploy({"from": account})

    # Upgrade proxy to new implementation
    upgrade(account, proxy, box2.address, proxy_admin)
    proxy_box2 = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # Make sure proxy uses new implementation
    proxy_box2.store(1, {"from": account})
    tx = proxy_box2.increment({"from": account})
    tx.wait(1)
    print(proxy_box2.retrieve())
