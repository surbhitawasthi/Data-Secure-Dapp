import ipfsApi
from os import path
import shutil

ipfs_client = ipfsApi.Client(host="https://ipfs.infura.io", port=5001)


def add_file(filepath):
    if path.exists(filepath):
        try:
            response = ipfs_client.add(filepath)
            return response, True
        except Exception as e:
            print(e)
            return {}, False
    else:
        return {}, False


def add_directory(directory_path):
    if path.exists(directory_path) and path.isdir(directory_path):
        try:
            response = ipfs_client.add(directory_path, recursive=True)
            return response, True
        except Exception as e:
            print(e)
            return [], False
    else:
        return [], False


def get_file(file_hash, location):
    try:
        ipfs_client.get(file_hash)
        shutil.move(file_hash, location)
    except Exception as e:
        print(e)
