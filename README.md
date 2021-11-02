# pancakebot

# 介绍
1. 支持买入卖出，挂单卖出，以及打新快进快出的功能
2. 仅支持bnb买入

# 安装
版本python3及以上

# 配置
在home目录创建config.json，模板参考config.json.tpl，配置好你的钱包地址和私钥就可以
# 命令参考：python main.py
![image](https://user-images.githubusercontent.com/7411249/139805893-019fd47f-bf29-4deb-ba6f-4528af927dfa.png)
## buy 购买代币
![image](https://user-images.githubusercontent.com/7411249/139807001-024ed9f0-c815-4fee-aa82-171e55b643a0.png)

参数“atprice”表示在特定代币/bnb价格的时候才会买入，否则会一直循环等待，类似挂单功能，若设置0则无限制

## sell 出售代币
![image](https://user-images.githubusercontent.com/7411249/139807040-9d88c928-83a4-4350-a884-d9cc9d781c4f.png)

参数“ap”，0.1表示10%，1表示100%，以此类推

参数“spb”，设置当前代币/bnb交易对的价格，当达到价格时会执行卖出，否则会一直循环，类似挂单功能，若设置0则无限制

## checkliq 检测交易对
![image](https://user-images.githubusercontent.com/7411249/138850853-62071905-b1a4-4457-af64-bd0263359a38.png)
## getpricebnb 检测代币与bnb的交易对价格
![image](https://user-images.githubusercontent.com/7411249/138851030-56528574-cbfe-4192-a43d-fe856e545ec3.png)
## makenew 打新快跑专用
![image](https://user-images.githubusercontent.com/7411249/139807090-0b465ffc-cd82-4edb-89b5-d6795c1918c8.png)


参数“incr”，0.1表示10%，1表示100%，以此类推，当`当前价格>=买入价格+买入价格*incr`时，该命令会把买入的bnb本金卖出，否则会一直循环，常见的打新保本策略

## attract 吸筹
![image](https://user-images.githubusercontent.com/7411249/139807126-31524a19-e77e-4bd6-bd68-bb77f633427b.png)


