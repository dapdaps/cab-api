from web3 import Web3


def is_dict_list(obj):
    if isinstance(obj, dict):
        return "dict"
    elif isinstance(obj, list):
        return "list"


def is_w3_address(address):
    try:
        Web3.to_checksum_address(address)
    except Exception:
        return False
    return True