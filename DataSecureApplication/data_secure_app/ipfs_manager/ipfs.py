import ipfsApi
from os import path
import os
import shutil
from pathlib import Path
from data_secure_app.main.web3_functions import get_key_for_user, get_key_for_user_by_doctor, get_list_of_user_files
from data_secure_app.encryption.encryption_engine import Encryptor
import time

ipfs_client = ipfsApi.Client(host="127.0.0.1", port=5001)
home = str(Path.home())


def add(filepath):
    if path.exists(filepath):
        try:
            start = time.time()
            response = ipfs_client.add(filepath)
            print('IPFS Storage Time: ', round((time.time() - start), 2))
            print(response)
            for r in response:
                if r['Name'] == filepath:
                    print('returning', r, True)
                    return r, True
            print('add: returning empty in for')
            return {}, False
        except Exception as e:
            print('add: returning empty in except', e)
            return {}, False
    else:
        print('add: returning empty in else')
        return {}, False


def add_file(filepath, user_address, doctor_address=None):
    if path.exists(filepath):
        if doctor_address:
            key_256_bit = get_key_for_user_by_doctor(doctor_address, user_address)
        else:
            key_256_bit = get_key_for_user(user_address)

        if key_256_bit == 'Err!':
            print('add_file: error in finding key')
            return {}, False

        enc = Encryptor(key=key_256_bit)
        start = time.time()
        new_filepath = enc.encrypt_file(file_name=filepath)
        print('Encryption Time: ', round((time.time() - start), 2))
        print(new_filepath)
        return add(new_filepath)
    else:
        print('add_file: filepath not exists:', filepath)
        return {}, False


def add_directory(directory_path):
    if path.exists(directory_path) and path.isdir(directory_path):
        try:
            response = ipfs_client.add(directory_path, recursive=True)
            for r in response:
                if r['Name'] == directory_path:
                    return r, True
            return {}, False
        except Exception as e:
            print(e)
            return [], False
    else:
        return [], False


def get(file_hash, location=home):
    try:
        start = time.time()
        ipfs_client.get(file_hash)
        print('IPFS Fetch Time: ', round((time.time() - start), 2))
        shutil.move(file_hash, location)
        return path.join(location, file_hash), True
    except Exception as e:
        print(e)
        return '', False


def get_file(filename, user_address, person_accessing_address, location='user_file_data_downloaded'):
    tmp = get_list_of_user_files(access_karne_wala=person_accessing_address, iski_files_hai=user_address)
    data, authorised = tmp[0], tmp[1]
    if not authorised:  # Ispe no trespassing Cannot access this user's file.
        return '403'
    else:
        for file_details in data:
            if file_details['filename'] == filename:
                file_hash = file_details['fileIPFSHash']
                file_path, err = get(file_hash, location=location)
                if not err:
                    return '500'  # Internal Server Error
                print(file_path)
                new_file_path = path.join(location, filename)
                os.rename(file_path, new_file_path)

                key_256_bit = get_key_for_user(user_address)

                if key_256_bit == 'Err!':
                    print('get_file: error in finding key')
                    return '500'  # Internal Server Error

                dec = Encryptor(key=key_256_bit)
                start = time.time()
                new_file_path = dec.decrypt_file(new_file_path)
                print('Decryption Time: ', round((time.time() - start), 2))
                # print(new_file_path)
                return new_file_path
        return '404'  # File not Found
