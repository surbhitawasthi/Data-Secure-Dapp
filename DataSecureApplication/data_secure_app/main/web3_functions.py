from web3.auto.infura.rinkeby import w3
import json
import os
import base64
import hashlib
from random import shuffle
import time


# CONTRACT_ADDRESS = '0x71C025B253137b451182311b670e8943eA144c6d'
# CONTRACT_ADDRESS = '0x874f9a0824d8650Afde8CC67Dd4fd72B1b4cDEd4'
# CONTRACT_ADDRESS = '0x51F6D40bd31C065A9a2BeC46eAEE68E57bE24F24'
# CONTRACT_ADDRESS = '0x356dd437cE5bAeeFbED1Ea6081179c95ffE833C3'
# CONTRACT_ADDRESS = '0x58D63739f49f4727162e904B241EF0e8AB9E6569'
# CONTRACT_ADDRESS = '0xa55Ce518A470f2C50DaF3c2ABdA04c01c3Bbc452'
CONTRACT_ADDRESS = '0xf4258C86202cD632eC32D65e855A453D83fCe89C'
CONTRACT_ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOCTOR_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_filename","type":"string"},{"internalType":"string","name":"_fileIPFSHash","type":"string"}],"name":"addFile","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"patientAddress","type":"address"},{"internalType":"address","name":"doctorAddress","type":"address"},{"internalType":"string","name":"_filename","type":"string"},{"internalType":"string","name":"_fileIPFSHash","type":"string"}],"name":"addFileByDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_userAddress","type":"address"},{"internalType":"string","name":"_username","type":"string"},{"internalType":"string","name":"_key","type":"string"},{"internalType":"bool","name":"_isDoc","type":"bool"}],"name":"addNewUser","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getCountOfMembersInMyRole","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userAddress","type":"address"}],"name":"getKeyForDoctor","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getKeyForUser","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getMemberOfMyRoleById","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userKaAddress","type":"address"}],"name":"getNumberOfFiles","outputs":[{"internalType":"uint256","name":"files","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"getRoleMember","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleMemberCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_externalUserAddress","type":"address"}],"name":"grantPermission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_externalUserAddress","type":"address"}],"name":"revokePermission","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_userKaAddress","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"viewFileOfAParticularUser","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


def add_new_user(admin_address, patient_address, patient_name, is_doc):
    admin_key = os.environ.get('admin_key')
    # print(admin_key)
    nonce = w3.eth.getTransactionCount(admin_address)
    chain_id = w3.eth.chainId

    tmp = list(patient_address)
    shuffle(tmp)
    key = ''.join(tmp)
    key_256_bit = hashlib.sha256(key.encode()).digest()
    encoded_key = base64.b64encode(key_256_bit).decode()

    tnx = contract.functions.addNewUser(patient_address, patient_name, encoded_key, is_doc).buildTransaction({
        'chainId': chain_id,
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    del tmp, key, key_256_bit, encoded_key

    try:
        signed_tnx = w3.eth.account.sign_transaction(tnx, private_key=admin_key)
    except Exception as e:
        print('signed_tnx\n', e)
        return False
    try:
        tnx_hash = w3.eth.sendRawTransaction(signed_tnx.rawTransaction)
    except Exception as e:
        print('tnx_hash\n', e)
        return False

    try:
        resp = w3.eth.waitForTransactionReceipt(tnx_hash)
        if resp is None:
            return False
        return True
    except Exception as e:
        print('add_new_user\n', e)
        return False


def grant_permission_in_bc(granted_by, granted_to):
    if granted_by == '0x6bAbcd1c5A89590cC10508e93dD59041ebF3f0B0':
        user_key = os.environ.get('doc1')
    elif granted_by == '0x4143c0C442D9Ba78846F062dbB4AAc7525FF6ce1':
        user_key = os.environ.get('pat1')
    elif granted_by == '0x81f01fD6F8dF4c2574689aC0D8c1ee34bE05De50':
        user_key = os.environ.get('pat2')
    elif granted_by == '0x02bcd51117Ff2FDC89f5F3b03d444f8a09e87a79':
        user_key = os.environ.get('pat3')
    elif granted_by == '0x99e19fa254D5919199B3F280C1A19410e17DBF69':
        user_key = os.environ.get('doc2')
    else:
        return False

    nonce = w3.eth.getTransactionCount(granted_by)
    chain_id = w3.eth.chainId

    tnx = contract.functions.grantPermission(granted_to).buildTransaction({
        'chainId': chain_id,
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    try:
        signed_tnx = w3.eth.account.sign_transaction(tnx, private_key=user_key)
    except Exception as e:
        print('signed_tnx\n', e)
        return False
    try:
        tnx_hash = w3.eth.sendRawTransaction(signed_tnx.rawTransaction)
    except Exception as e:
        print('tnx_hash\n', e)
        return False

    try:
        resp = w3.eth.waitForTransactionReceipt(tnx_hash)
        if resp is None:
            return False
        return True
    except Exception as e:
        print('error_in_grant_perm\n', e)
        return False


def revoke_permission_in_bc(revoked_by, revoked_for):
    if revoked_by == '0x6bAbcd1c5A89590cC10508e93dD59041ebF3f0B0':
        user_key = os.environ.get('doc1')
    elif revoked_by == '0x4143c0C442D9Ba78846F062dbB4AAc7525FF6ce1':
        user_key = os.environ.get('pat1')
    elif revoked_by == '0x81f01fD6F8dF4c2574689aC0D8c1ee34bE05De50':
        user_key = os.environ.get('pat2')
    elif revoked_by == '0x02bcd51117Ff2FDC89f5F3b03d444f8a09e87a79':
        user_key = os.environ.get('pat3')
    elif revoked_by == '0x99e19fa254D5919199B3F280C1A19410e17DBF69':
        user_key = os.environ.get('doc2')
    else:
        return False

    nonce = w3.eth.getTransactionCount(revoked_by)
    chain_id = w3.eth.chainId

    tnx = contract.functions.revokePermission(revoked_for).buildTransaction({
        'chainId': chain_id,
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    try:
        signed_tnx = w3.eth.account.sign_transaction(tnx, private_key=user_key)
    except Exception as e:
        print('signed_tnx\n', e)
        return False
    try:
        tnx_hash = w3.eth.sendRawTransaction(signed_tnx.rawTransaction)
    except Exception as e:
        print('tnx_hash\n', e)
        return False

    try:
        resp = w3.eth.waitForTransactionReceipt(tnx_hash)
        if resp is None:
            return False
        return True
    except Exception as e:
        print('error_in_revoke_perm\n', e)
        return False


def add_file_hash_to_bc(address, filename, fileIPFSHash):
    if address == '0x6bAbcd1c5A89590cC10508e93dD59041ebF3f0B0':
        user_key = os.environ.get('doc1')
    elif address == '0x4143c0C442D9Ba78846F062dbB4AAc7525FF6ce1':
        user_key = os.environ.get('pat1')
    elif address == '0x81f01fD6F8dF4c2574689aC0D8c1ee34bE05De50':
        user_key = os.environ.get('pat2')
    elif address == '0x02bcd51117Ff2FDC89f5F3b03d444f8a09e87a79':
        user_key = os.environ.get('pat3')
    elif address == '0x99e19fa254D5919199B3F280C1A19410e17DBF69':
        user_key = os.environ.get('doc2')
    else:
        return False

    nonce = w3.eth.getTransactionCount(address)
    chain_id = w3.eth.chainId

    tnx = contract.functions.addFile(filename, fileIPFSHash).buildTransaction({
        'chainId': chain_id,
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    try:
        signed_tnx = w3.eth.account.sign_transaction(tnx, private_key=user_key)
    except Exception as e:
        print('signed_tnx\n', e)
        return False
    try:
        start = time.time()
        tnx_hash = w3.eth.sendRawTransaction(signed_tnx.rawTransaction)
    except Exception as e:
        print('tnx_hash\n', e)
        return False

    try:
        resp = w3.eth.waitForTransactionReceipt(tnx_hash)
        print('Mining Time add_file_hash_to_bc: ', round((time.time() - start), 2))
        if resp is None:
            return False
        return True
    except Exception as e:
        print('error_in_add_file_hash\n', e)
        return False


def add_file_hash_to_bc_by_doc(doctor_address, patient_address, filename, fileIPFSHash):
    if doctor_address == '0x6bAbcd1c5A89590cC10508e93dD59041ebF3f0B0':
        user_key = os.environ.get('doc1')
    elif doctor_address == '0x99e19fa254D5919199B3F280C1A19410e17DBF69':
        user_key = os.environ.get('doc2')
    else:
        return False

    nonce = w3.eth.getTransactionCount(doctor_address)
    chain_id = w3.eth.chainId

    tnx = contract.functions.addFileByDoctor(patient_address, doctor_address, filename, fileIPFSHash).buildTransaction({
        'chainId': chain_id,
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    try:
        signed_tnx = w3.eth.account.sign_transaction(tnx, private_key=user_key)
    except Exception as e:
        print('signed_tnx\n', e)
        return False
    try:
        start = time.time()
        tnx_hash = w3.eth.sendRawTransaction(signed_tnx.rawTransaction)
    except Exception as e:
        print('tnx_hash\n', e)
        return False

    try:
        resp = w3.eth.waitForTransactionReceipt(tnx_hash)
        print('Mining Time add_file_hash_to_bc_by_doc: ', round((time.time() - start), 2))
        if resp is None:
            return False
        return True
    except Exception as e:
        print('error in doc-pat file add\n', e)
        return False


def get_list_of_user_with_my_permission(address):
    try:
        no_of_people = contract.functions.getCountOfMembersInMyRole().call({'from': address})
        print(no_of_people, address)
        if no_of_people >= 1000000000000000:
            return [], False
    except Exception as e:
        print('error in get list of users with my permission\n', e)
        return [], False

    files = []
    for i in range(no_of_people):
        tmp = {}
        try:
            ret = contract.functions.getMemberOfMyRoleById(int(i)).call({'from': address})
        except Exception as e:
            print('while looping in people\n', e)
            return [], False
        tmp['name'] = ret[1]
        tmp['address'] = ret[0]
        files.append(tmp)

    return files, True


def get_list_of_user_files(access_karne_wala, iski_files_hai):
    try:
        no_of_files = contract.functions.getNumberOfFiles(iski_files_hai).call({'from': access_karne_wala})
        if no_of_files >= 1000000000000000:
            return [], False
    except Exception as e:
        print('error in get list of user files\n', e)
        return [], False

    files = []
    start = time.time()
    for i in range(no_of_files):
        tmp = {}
        try:
            ret = contract.functions.viewFileOfAParticularUser(iski_files_hai, i).call({'from': access_karne_wala})
        except Exception as e:
            print('while looping in file\n', e)
            return [], False
        tmp['filename'] = ret[0]
        tmp['fileIPFSHash'] = ret[1]
        files.append(tmp)
    print('Mining Time get_list_of_user_files: ', round((time.time() - start), 2))
    return files, True


def get_balance(address):
    try:
        bal = float(round(w3.fromWei(w3.eth.getBalance(address), 'ether'), 4))
        return str(bal) + ' ETH'
    except Exception as e:
        print('error in get list of user files\n', e)
        return 'Err!'


def get_file_count(address):
    try:
        no_of_files = contract.functions.getNumberOfFiles(address).call({'from': address})
        if no_of_files >= 1000000000000000:
            return 'Err!'
        else:
            return no_of_files
    except Exception as e:
        print('error in get list of user files\n', e)
        return 'Err!'


def get_key_for_user(address):
    try:
        encoded_key = contract.functions.getKeyForUser().call({'from': address})
        print(encoded_key)
        decoded_key = base64.b64decode(encoded_key)
        return decoded_key
    except OverflowError:
        print('Not authorised get_key_for_user')
        return 'Err!'
    except Exception as e:
        print('get_key_for_user:', '\n', e)
        return 'Err!'


def get_key_for_user_by_doctor(doctor_address, address):
    user_key = None
    if doctor_address == '0x6bAbcd1c5A89590cC10508e93dD59041ebF3f0B0':
        user_key = os.environ.get('doc1')
    elif doctor_address == '0x99e19fa254D5919199B3F280C1A19410e17DBF69':
        user_key = os.environ.get('doc2')

    if not user_key:
        return 'Err!'

    try:
        encoded_key = contract.functions.getKeyForDoctor(address).call({'from': doctor_address})
        print(encoded_key)
        decoded_key = base64.b64decode(encoded_key)
        return decoded_key
    except OverflowError:
        print('Not authorised get_key_for_user_by_doctor')
        return 'Err!'
    except Exception as e:
        print('get_key_for_user_by_doctor:', '\n', e)
        return 'Err!'
