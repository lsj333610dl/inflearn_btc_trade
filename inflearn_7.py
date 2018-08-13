
import requests
import time
import time, base64, hmac, hashlib, requests, json
import telegram

apikey = '3fcdf0c7-078b-43b0-a09b-ffc6143573e9'
secret = '9akSvT8klk3SxE0YneRHS+WVk3Lv462SNt/jM9bRa8S5fMiXxIwxYPk5teMrGxz6Xxuq+MBcuIIhUK0GOz6mVg=='

my_token = '612185624:AAHioMOPPjQejvv99aVYsocKlQsCISx7cE8'
chat_id = '341006364'

bot = telegram.Bot(token = my_token)

message = '트레이딩 봇 시작!'

bot.sendMessage(chat_id=chat_id, text=message)

while True:
    nonce = str(time.time())
    method = 'POST'
    request_path = '/orders'

    now_time = round(time.time() * 1000)
    start = int(now_time)-60*50*1000
    end = int(now_time)

    r = requests.get('https://api.gopax.co.kr/trading-pairs/BTC-KRW/candles?start='+str(start)+'&end='+str(end)+'&interval=60')
    #
    print(len(r.json()))

    arr = r.json()
    close_price_list = []
    for ar in arr:
        close_price_list.append(ar[4])
        # print(ar)

    # print(close_price_lsit)
    # [
    #   [
    #     <Time>,
    #     <Low>,
    #     <High>,
    #     <Open>,
    #     <Close>,
    #     <Volume>
    #   ],
    #   [
    #     1521004080000,
    #     10081000,
    #     10081000,
    #     10081000,
    #     10081000,
    #     0.01
    #   ]
    # ]

    avg_min_15 = sum(close_price_list[-15:]) / 15
    avg_min_50 = sum(close_price_list[-50:]) / 50
    #
    print(avg_min_15)
    print(avg_min_50)

    is_buy = False
    if avg_min_15 > avg_min_50 * 1.004 and is_buy == False:
        request_body = {
            "amount": 0.001,
            "price": close_price_list[-1],
            "side": "buy",
            "tradingPairName": "BTC-KRW",
            "type": "limit"
        };

        # 필수 정보를 연결하여 prehash 문자열을 생성함
        what = nonce + method + request_path + json.dumps(request_body, sort_keys=True)
        # base64로 secret을 디코딩함
        key = base64.b64decode(secret)
        # hmac으로 필수 메시지에 서명하고
        signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
        # 그 결과물을 base64로 인코딩함
        signature_b64 = base64.b64encode(signature.digest())

        custom_headers = {
            'API-Key': apikey,
            'Signature': signature_b64,
            'Nonce': nonce
        }

        req = requests.post(url='https://api.gopax.co.kr' + request_path, headers=custom_headers, json=request_body)
        is_buy = True

        message = '종목 : 비트코인 \n 가격 : {} \n 수량 : {}'.format(close_price_list[-1], 0.001)

        bot.sendMessage(chat_id=chat_id, text=message)

        print('매수')

    if avg_min_50 > avg_min_15 and is_buy == True:
        request_body = {
            "amount": 0.001,
            "price": close_price_list[-1],
            "side": "sell",
            "tradingPairName": "BTC-KRW",
            "type": "limit"
        };

        # 필수 정보를 연결하여 prehash 문자열을 생성함
        what = nonce + method + request_path + json.dumps(request_body, sort_keys=True)
        # base64로 secret을 디코딩함
        key = base64.b64decode(secret)
        # hmac으로 필수 메시지에 서명하고
        signature = hmac.new(key, str(what).encode('utf-8'), hashlib.sha512)
        # 그 결과물을 base64로 인코딩함
        signature_b64 = base64.b64encode(signature.digest())

        custom_headers = {
            'API-Key': apikey,
            'Signature': signature_b64,
            'Nonce': nonce
        }

        req = requests.post(url='https://api.gopax.co.kr' + request_path, headers=custom_headers, json=request_body)

        is_buy = False

        message = '종목 : 비트코인 \n 가격 : {} \n 수량 : {}'.format(close_price_list[-1],0.001)

        bot.sendMessage(chat_id=chat_id, text=message)

        print('매도')

    time.sleep(5)



