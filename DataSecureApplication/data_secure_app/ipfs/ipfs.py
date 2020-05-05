import ipfsApi
from os import path
import shutil
from pathlib import Path

ipfs_client = ipfsApi.Client(host="https://ipfs.infura.io", port=5001)
home = str(Path.home())


def add_file(filepath):
    if path.exists(filepath):
        try:
            response = ipfs_client.add(filepath)
            for r in response:
                if r['Name'] == filepath[1:]:
                    return r, True
            return {}, False
        except Exception as e:
            print(e)
            return {}, False
    else:
        return {}, False


def add_directory(directory_path):
    if path.exists(directory_path) and path.isdir(directory_path):
        try:
            response = ipfs_client.add(directory_path, recursive=True)
            for r in response:
                if r['Name'] == directory_path[1:]:
                    return r, True
            return {}, False
        except Exception as e:
            print(e)
            return [], False
    else:
        return [], False


def get_file(file_hash, location=home):
    try:
        ipfs_client.get(file_hash)
        shutil.move(file_hash, location)
        return True
    except Exception as e:
        print(e)
        return False
