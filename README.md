# pancakebot

# 介绍
1. 支持买入卖出，挂单卖出，以及打新快进快出的功能
2. 仅支持bnb买入

# 配置
在home目录创建config.json，模板参考config.json.tpl，配置好你的钱包地址和私钥就可以
# 命令参考：python main.py
![image](https://user-images.githubusercontent.com/7411249/138850134-267d7e57-8699-41aa-bcb9-423e2b433759.png)
## buy 购买代币
![image](https://user-images.githubusercontent.com/7411249/138850520-f530ec9e-2dd8-42e0-9776-cfebe7a40638.png)
## sell 出售代币
![image](https://user-images.githubusercontent.com/7411249/138850629-f8a2409d-d311-4a24-836d-44ca92aac5fd.png)

参数“ap”，0.1表示10%，1表示100%，以此类推

参数“spb”，设置当前代币/bnb交易对的价格，当达到价格时会执行卖出，否则会一直循环，若设置0则直接卖出
## checkliq 检测交易对
![image](https://user-images.githubusercontent.com/7411249/138850853-62071905-b1a4-4457-af64-bd0263359a38.png)
## getpricebnb 检测代币与bnb的交易对价格
![image](https://user-images.githubusercontent.com/7411249/138851030-56528574-cbfe-4192-a43d-fe856e545ec3.png)
## makenew 打新快跑专用
![image](https://user-images.githubusercontent.com/7411249/138851186-ba0c9730-40d3-43c5-a3f7-4f1da579ba17.png)

参数“incr”，0.1表示10%，1表示100%，以此类推，当`当前价格>=买入价格+买入价格*incr`时，该命令会把买入的bnb本金卖出，否则会一直循环，常见的打新保本策略
