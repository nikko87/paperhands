import requests as re
import pandas as pd

NFT_CONTRACT = '0x6137cBEf171F49c58f92Fa696F8Fe053688fC93e'
STAKE_CONTRACT = '0x569Cc6a45a008D94473C2a7F476e6C54A9354A3F'

def handle_minted_only(df_minted: pd.DataFrame) -> pd.DataFrame:
    df_minted = df_minted[(df_minted.value > 0.0) & (df_minted.value % 0.075 == 0)]
    df_minted = df_minted[df_minted.to_address.str.contains(NFT_CONTRACT, case=False)]
    return df_minted

def handle_staked_only(df_staked: pd.DataFrame) -> pd.DataFrame:
    df_staked = df_staked[df_staked.to_address.str.contains(STAKE_CONTRACT, case=False)]
    return df_staked

def handle_wallet(df_wallet: pd.DataFrame, wallet: str) ->  pd.DataFrame:
    df_wallet = df_wallet[df_wallet.from_address.str.contains(wallet, case=False)]
    return df_wallet
          

response = re.get('https://api.covalenthq.com/v1/1/address/0x6137cBEf171F49c58f92Fa696F8Fe053688fC93e/transactions_v2/?quote-currency=USD&format=JSON&page-size=40000&no-logs=true&key=ckey_6a1628ef564d4e5e957df3d982e')

js = response.json()['data']['items']
df = pd.DataFrame.from_dict(js)
df = df.astype(
    {
        'value': 'float64',
        'from_address': 'string',
        'to_address': 'string'
    }
)
df = df[['tx_hash', 'from_address', 'to_address', 'value', 'value_quote', 'gas_quote']]
df.value = df.value / 10 ** 18 # valor em ETH

# my_wallet = '0x55B37193a91FBd38806b699C02df8C65b9d45500'
# df_mywallet = handle_wallet(df, my_wallet)
# print(df_mywallet)

df_minted_only = handle_minted_only(df)
df_staked_only = handle_staked_only(df)

with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Transactions')
    df_minted_only.to_excel(writer, sheet_name='Minted only')
    df_staked_only.to_excel(writer, sheet_name='Staked only')




