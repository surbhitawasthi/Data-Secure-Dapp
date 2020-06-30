import requests
import time
import os


def get_transaction_details(user_address):
    query_url_structure = 'http://api-rinkeby.etherscan.io/api?module=account&action=txlist&' \
                          'address={0}&startblock=0&endblock=99999999&sort=asc' \
                          '&apikey=' + os.environ.get('ETH_KEY')

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    query_url = query_url_structure.format(user_address)

    try:
        resp = requests.get(query_url, headers=headers)
        # print(resp.status_code)
        if resp.status_code == 200:
            data = resp.json()
            data = data['result']
            transactions = []
            for tnx in data:
                tmp_dict = {}
                tmp_dict['txn_hash'] = tnx['hash']
                tmp_dict['txn_hash_link'] = 'https://rinkeby.etherscan.io/tx/' + tnx['hash']
                tmp_dict['age'] = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(tnx['timeStamp'])))
                tmp_dict['value'] = float(tnx['value'])/(10**18)
                transactions.append(tmp_dict)
            return transactions
        else:
            return []
    except Exception as e:
        print('get_transaction_details:\n', e)
        return []
