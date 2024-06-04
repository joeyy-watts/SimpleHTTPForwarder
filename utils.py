import re
import subprocess


def format_mac_address(mac_addr: str):
    final_addr = ''
    for char_idx, char in enumerate(mac_addr):
        if (char_idx + 1) % 2 == 0 and char_idx < 11:
            final_addr = final_addr + char + ':'
        else:
            final_addr = final_addr + char
    return final_addr.lower()


def load_mac_mapping(conf_name="mac_addrs.conf"):
    """
    loads the MAC address to alias mapping from config file
    :return: dict with:
        - key: device alias
        - value: device MAC address
    """
    # open config on each call to allow for hot config change
    conf = open(f'./{conf_name}', 'r')
    dict = {}
    for each in conf:
        alias, mac = each.split(':')
        mac = format_mac_address(mac)
        dict[alias] = mac.strip('\n')

    return dict

def get_ip_from_alias(alias: str):
    mapping = load_mac_mapping()

    if alias not in mapping:
        raise Exception(f"No device found with alias {alias}!")

    return get_local_ip(mapping[alias])


def get_local_ip(mac_address: str):
    cmd = f"arp -an | grep {mac_address}"
    print(f"getting main led controller ip with command :: {cmd}")
    ret = subprocess.check_output((cmd), shell=True, stderr=subprocess.STDOUT).decode()

    print(f'ret is {ret}')
    pattern = "([0-9.])+"
    match = re.search(pattern, ret)
    return match.group()


def refresh_arp_cache():
    cmd = 'nmap -sP 192.168.1.0/24'
    print(f'refreshing arp cache with command :: {cmd}')
    subprocess.run(cmd.split(' '))
