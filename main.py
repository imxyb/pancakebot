import decimal
import json
import os
import time

import click
from web3 import Web3

bnb_address = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
usdt_address_token = "0x55d398326f99059ff775485246999027b3197955"


class InsufficientBalance(Exception):
    pass


class TXFail(Exception):
    pass


class PancakeSwapBot:
    def __init__(self, target_address):
        bsc = "https://bsc-dataseed.binance.org/"
        self.web3 = Web3(Web3.HTTPProvider(bsc))

        self.pancake_factory_address = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
        self.pancake_router_address = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
        router_abi = """
[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
    """
        factory_abi = """
[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]
        """
        self.pancake_router_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(self.pancake_router_address), abi=router_abi)
        self.pancake_factory_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(self.pancake_factory_address), abi=factory_abi)

        # 默认bnb
        self.bnb_token_address = self.web3.toChecksumAddress(bnb_address)
        self.usdt_token_address = self.web3.toChecksumAddress(usdt_address_token)
        bnbabi = """
        [{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]
        """
        self.from_token_contract = self.web3.eth.contract(address=self.bnb_token_address, abi=bnbabi)

        config = self.load_config()
        self.from_address = config['from_address']
        self.private_key = config['private_key']

        self.target_address = self.web3.toChecksumAddress(target_address)
        self.target_abi = """
        [{"inputs":[{"internalType":"string","name":"_NAME","type":"string"},{"internalType":"string","name":"_SYMBOL","type":"string"},{"internalType":"uint256","name":"_DECIMALS","type":"uint256"},{"internalType":"uint256","name":"_supply","type":"uint256"},{"internalType":"uint256","name":"_txFee","type":"uint256"},{"internalType":"uint256","name":"_lpFee","type":"uint256"},{"internalType":"uint256","name":"_MAXAMOUNT","type":"uint256"},{"internalType":"uint256","name":"SELLMAXAMOUNT","type":"uint256"},{"internalType":"address","name":"routerAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numTokensSellToAddToLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"swapNumber","type":"uint256"}],"name":"setNumTokensSellToAddToLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
        """
        self.target_contract = self.web3.eth.contract(address=self.target_address, abi=self.target_abi)

    @staticmethod
    def load_config():
        with open(os.path.join(os.environ['HOME'], 'config.json')) as f:
            return json.load(f)

    def check_liq(self):
        pair = self.pancake_factory_contract.functions.getPair(self.bnb_token_address, self.target_address).call()
        try:
            pair.index("0x0000000")
            return None, False
        except Exception as e:
            return pair, True

    def get_bnb_balance(self):
        return self.from_token_contract.functions.balanceOf(self.web3.toChecksumAddress(self.from_address)).call()

    def get_pair_bnb_balance(self, pair_address):
        return self.from_token_contract.functions.balanceOf(self.web3.toChecksumAddress(pair_address)).call()

    def buy(self, amount_bnb, pair="bnb"):
        value = self.web3.toWei(amount_bnb, 'ether')
        path = [self.bnb_token_address, self.target_address]
        if pair == "usdt":
            path = [self.bnb_token_address, self.usdt_token_address, self.target_address]
        txn = self.pancake_router_contract.functions.swapExactETHForTokens(
            0,
            path,
            self.web3.toChecksumAddress(self.from_address),
            (int(time.time()) + 1000000)
        ).buildTransaction({
            'from': self.from_address,
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })

        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        try:
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=150)
            if receipt['status'] == 0:
                raise TXFail('交易hash状态失败，建议重试')
            print("买入完成，查看结果：https://bscscan.com/tx/{}".format(self.web3.toHex(tx_hash)))
        except Exception as e:
            raise e

    def get_balance(self):
        return self.target_contract.functions.balanceOf(self.web3.toChecksumAddress(self.from_address)).call()

    def get_decimals(self):
        return int(self.target_contract.functions.decimals().call())

    def get_price_bnb(self):
        pair = self.pancake_router_contract.functions.getAmountsOut(1 * pow(10, self.get_decimals()),
                                                                    [self.target_address,
                                                                     self.bnb_token_address]).call()
        return self.web3.fromWei(pair[1], 'ether')

    def get_price_usdt(self):
        pair = self.pancake_router_contract.functions.getAmountsOut(1 * pow(10, self.get_decimals()),
                                                                    [self.target_address,
                                                                     self.usdt_token_address]).call()
        return self.web3.fromWei(pair[1], 'ether')

    def get_target_amount_from_bnb(self, amount_bnb):
        pair = self.pancake_router_contract.functions.getAmountsOut(self.web3.toWei(amount_bnb, 'ether'),
                                                                    [self.bnb_token_address,
                                                                     self.target_address]).call()
        return pair[1]

    def get_target_amount_from_usdt(self, amount_usdt):
        pair = self.pancake_router_contract.functions.getAmountsOut(self.web3.toWei(amount_usdt, 'ether'),
                                                                    [self.usdt_token_address,
                                                                     self.target_address]).call()
        return pair[1]

    def approve(self):
        tx = self.target_contract.functions.approve(self.pancake_router_address, self.get_balance()).buildTransaction({
            'from': self.from_address,
            'gasPrice': self.web3.toWei('5', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        try:
            self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=150)
            print("approve完成，查看结果：https://bscscan.com/tx/{}".format(self.web3.toHex(tx_hash)))
        except Exception as e:
            raise e

    def sell(self, amount, amount_bnb, amount_percent, pair="bnb"):
        txn_amount = 0

        # 授权
        self.approve()

        if amount > 0:
            txn_amount = int(amount * pow(10, self.get_decimals()))
        elif amount_percent > 0:
            balance = self.get_balance()
            bw = self.web3.fromWei(balance, 'ether') * decimal.Decimal(amount_percent)
            txn_amount = self.web3.toWei(bw, 'ether')
        elif amount_bnb > 0:
            txn_amount = self.get_target_amount_from_bnb(amount_bnb)

        path = [self.target_address, self.bnb_token_address],
        if pair == "usdt":
            path = [self.target_address, self.usdt_token_address, self.bnb_token_address]

        txn = self.pancake_router_contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            txn_amount,
            0,
            path,
            self.from_address,
            (int(time.time()) + 1000000)
        ).buildTransaction({
            'from': self.from_address,
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        try:
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=150)
            if receipt['status'] == 0:
                raise TXFail('交易hash状态失败，建议重试')
            print("卖出完成，查看结果：https://bscscan.com/tx/{}".format(self.web3.toHex(tx_hash)))
        except Exception as e:
            raise e


@click.group()
def cli():
    pass


@click.command()
@click.option('--ta', help='目标token')
def getpricebnb(ta):
    bot = PancakeSwapBot(ta)
    print(bot.get_price_bnb())


@click.command()
@click.option('--ta', help='目标token')
def getpriceusdt(ta):
    bot = PancakeSwapBot(ta)
    print(bot.get_price_usdt())


@click.command()
@click.option('--ta', help='目标token')
@click.option('--ab', help='买入的bnb数量', type=float)
@click.option('--at', help='买入的代币数量', type=float)
@click.option('--atprice', help='设定买入价，只有等于或小于买入价才买入', type=float, default=0)
@click.option('--maxbuy', help='连续买n次', type=int, default=1)
@click.option('--pair', help='挂单交易对,默认bnb', type=str, default="bnb")
def buy(ta, ab, at, atprice, maxbuy, pair):
    while maxbuy > 0:
        bot = PancakeSwapBot(ta)
        try:
            if pair == "usdt":
                pair_price = bot.get_price_usdt()
            else:
                pair_price = bot.get_price_bnb()
            if 0 < atprice < pair_price:
                print('当前价格:{}>设定买入价:{}，放弃'.format(pair_price, atprice))
                continue
            if at is not None and ab is None:
                ab = decimal.Decimal(at) * pair_price
        except Exception as e:
            print('bsc节点不稳定,err:{}'.format(e))
            continue
        try:
            bot.buy(ab, pair)
            maxbuy -= 1
        except TXFail:
            print('交易偶发失败，重试')
            continue
        except Exception as e:
            print('买入失败,err:{}'.format(e))
            continue
    print("购买完成")


@click.command()
@click.option('--ta', help='目标token')
@click.option('--ab', help='买入的bnb数量', type=float)
@click.option('--lp', help='低于上次买入价格的多少比例将再次买入,0~1,例如0.1表示低于上次价格的10%', type=float)
@click.option('--minip', help='最低吸筹价，表示当现价格低于设置价格时会连续买入', type=float)
@click.option('--maxbuy', help='最多买入次数', type=int, default=1)
@click.option('--atprice', help='设定买入价，只有等于或小于买入价才买入', type=float, default=0)
def bdp(ta, ab, lp, minip, maxbuy, atprice):
    prev_bnb_price = 0
    lp = decimal.Decimal(lp)
    while maxbuy > 0:
        bot = PancakeSwapBot(ta)
        try:
            bnb_price = bot.get_price_bnb()
            if 0 < atprice < bnb_price:
                print('当前价格:{}>设定买入价:{}，放弃'.format(bnb_price, atprice))
                continue
        except Exception as e:
            print('bsc节点不稳定,err:{}'.format(e))
            continue
        next_price = prev_bnb_price - prev_bnb_price * lp
        if next_price != 0 and next_price <= minip:
            next_price = minip
        if prev_bnb_price == 0 or (bnb_price <= minip) or (bnb_price <= next_price):
            try:
                bot.buy(ab)
                prev_bnb_price = bot.get_price_bnb()
                print('买入成功,买入价格:{}'.format(prev_bnb_price))
                maxbuy -= 1
                continue
            except InsufficientBalance:
                print('余额不足，请充值')
                continue
            except TXFail:
                print('交易偶发失败，重试')
                continue
            except Exception as e:
                print('买入失败,err:{}'.format(e))
                continue
        else:
            try:
                print('当前价格:{},下次吸筹价格:{},剩下买入次数:{}'.format(bot.get_price_bnb(), next_price, maxbuy))
            except Exception as e:
                print('bsc节点不稳定,err:{}'.format(e))
                continue
    else:
        print('达到最大买入次数，退出')


@click.command()
@click.option('--ta', help='目标token')
@click.option('--amount', help='卖出数量', default=0, type=float)
@click.option('--ab', help='卖出的bnb数量', default=0, type=float)
@click.option('--ap', help='卖出比例，0~1', default=0, type=float)
@click.option('--maxsell', help='连续卖出次数', default=1, type=float)
@click.option('--pair', help='交易对，默认bnb', default="bnb", type=str)
@click.option('--atprice', help='设定卖出价，只有等于或大于卖出价才买入', type=float, default=None)
def sell(ta, amount, ab, ap, maxsell, pair, atprice):
    bot = PancakeSwapBot(ta)
    while maxsell > 0:
        try:
            if pair == "usdt":
                pair_price = bot.get_price_usdt()
            else:
                pair_price = bot.get_price_bnb()

            if atprice is not None and pair_price < atprice:
                print('当前价格:{}<设定卖出价:{}，放弃'.format(pair_price, atprice))
                continue
            bot.sell(amount, ab, ap, pair)
            maxsell -= 1
        except TXFail:
            print('交易偶发失败，重试')
            continue
        except Exception as e:
            print('卖出失败,err:{}'.format(e))
            continue


@click.command()
@click.option('--ta', help='目标token')
def checkliq(ta):
    bot = PancakeSwapBot(ta)
    _, exist = bot.check_liq()
    if not exist:
        print('交易对已建立')
    else:
        print('交易对未建立')


# 适用打新，设定翻倍出本
@click.command()
@click.option('--ta', help='目标token', required=True)
@click.option('--bab', help='买入bnb数量', type=float, required=True)
@click.option('--incr', help='达到涨幅卖出,0~10000', type=float, default=1)
@click.option('--minliq', help='池子最小bnb数量，当小于该bnb数则认为该币种尚未开盘或被注入私人流动车', type=float, default=0)
@click.option('--afterbn', help='监测到流动车会记录当前区块高度，在此区块的n个区块后再购买，防杀', type=int, required=False)
def makenew(ta, bab, incr, minliq, afterbn):
    bot = PancakeSwapBot(ta)

    while True:
        pair, exist = bot.check_liq()
        if exist:
            break

        print('尚未建立交易对')
        time.sleep(1)
        continue

    print("交易对已经建立")

    # 监测流动池大小，小于设置的最小池子bnb数则继续循环等待
    if pair is not None:
        while True:
            pair_bnb_balance = bot.get_pair_bnb_balance(pair) // pow(10, 18)
            if pair_bnb_balance > minliq:
                break
            print('池子bnb数:{}<最小开盘池子bnb数:{}'.format(pair_bnb_balance, minliq))
            time.sleep(1)
            continue

    start_block_number = bot.web3.eth.get_block_number()
    can_buy_block_number = start_block_number + afterbn
    print('交易对已建立, 当前区块:{}, 可购买区块:{}，进入购买过程'.format(start_block_number, can_buy_block_number))
    while True:
        # 防杀
        if afterbn is not None:
            current_block_number = bot.web3.eth.get_block_number()
            if current_block_number < can_buy_block_number:
                print("当前区块:{}<可购买区块:{},等待...", current_block_number, can_buy_block_number)
                continue

        try:
            bot.buy(bab)
            break
        except TXFail:
            print('买入偶发失败，重试')
            continue
        except Exception as e:
            print('可能尚未开盘,err:{}'.format(e))
            time.sleep(1)
            continue

    price_bnb = bot.get_price_bnb()
    sell_principal = price_bnb + price_bnb * decimal.Decimal(incr)

    print('当前币量:{}，买入价格:{},出本价格:{}'.format(bot.get_balance() // pow(10, bot.get_decimals()),
                                           price_bnb, sell_principal))

    sell_pass = False
    while True:
        cur_price_bnb = bot.get_price_bnb()
        if cur_price_bnb >= sell_principal:
            print('达到出本价格，开始卖出本金')
            while True:
                try:
                    bot.sell(0, bab, 0, 0)
                    sell_pass = True
                    break
                except TXFail:
                    print('卖出偶发失败，重试')
                    continue
                except Exception as e:
                    print('卖出失败,err:{}'.format(e))
                    break
            break
        print('未达到出本价格{},当前价格:{}'.format(sell_principal, cur_price_bnb))
        continue

    if sell_pass:
        print('已出本，当前剩余币量:{}'.format(bot.get_balance() // pow(10, bot.get_decimals())))
    else:
        print('出本失败，请手动卖出')


@click.command()
@click.option('--ta', help='目标token', required=True)
def getbalance(ta):
    bot = PancakeSwapBot(ta)
    print(bot.get_balance() / pow(10, bot.get_decimals()))


@click.command()
@click.option('--ta', help='目标token', required=True)
@click.option('--ab', help='波段金额bnb', type=float, required=True)
@click.option('--buyatprice', help='购买价格', type=float, required=True)
@click.option('--sellatprice', help='出售价格', type=float, required=True)
@click.option('--times', help='波段次数', type=int, required=False, default=1)
@click.option('--pair', help='交易对,默认bnb', type=str, required=False, default='bnb')
def band(ta, ab, buyatprice, sellatprice, times, pair):
    bot = PancakeSwapBot(ta)
    while times > 0:
        try:
            if pair == "usdt":
                pair_price = bot.get_price_usdt()
            else:
                pair_price = bot.get_price_bnb()

            if pair_price > buyatprice:
                print('当前价格:{}>设定买入价:{}，放弃'.format(pair_price, buyatprice))
                continue

            bot.buy(ab, pair)
            print("购买成功")
            while True:
                if pair == "usdt":
                    pair_price = bot.get_price_usdt()
                else:
                    pair_price = bot.get_price_bnb()

                if pair_price < sellatprice:
                    print('当前价格:{}<设定卖出价:{}，放弃'.format(pair_price, sellatprice))
                    continue
                bot.sell(0, ab, 0, pair)
                print("出售成功")
            print("完成一次波段")
            times -= 1
        except TXFail:
            print('交易偶发失败，重试')
            continue
        except Exception as e:
            print('波段失败,err:{}'.format(e))
            continue
    print("退出波段")


cli.add_command(buy)
cli.add_command(sell)
cli.add_command(getpricebnb)
cli.add_command(getpriceusdt)
cli.add_command(checkliq)
cli.add_command(makenew)
cli.add_command(bdp)
cli.add_command(getbalance)
cli.add_command(band)

if __name__ == '__main__':
    cli()
