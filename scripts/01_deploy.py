from scripts.helpful_scripts import *
from brownie import network, config, Box, ProxyAdmin

def main():

    # Deploy the Proxy Contract
    account = getAccount()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})
    
    proxy_admin = ProxyAdmin.deploy({"from": account})
    
