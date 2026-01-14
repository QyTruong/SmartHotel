import json
import uuid
import requests
import hmac
import hashlib


endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
accessKey = "F8BBA842ECF85"
secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
orderInfo = "pay with MoMo"
partnerCode = "MOMO"
redirectUrl = "https://127.0.0.1:8000"
ipnUrl = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
extraData = ""
partnerName = "MoMo Payment"
storeId = "Test Store"
orderGroupId = ""
autoCapture = True
lang = "vi"
requestType = "payWithMethod"


def create_signature(raw_signature):
    # signature
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(raw_signature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    return signature


def create_momo_payment(total_amount):
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())


    raw_signature = "accessKey=" + accessKey + "&amount=" + str(int(total_amount)) + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId \
                    + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl \
                    + "&requestId=" + requestId + "&requestType=" + requestType

    signature = create_signature(raw_signature=raw_signature)


    data = {
        "partnerCode": partnerCode,
        "requestId": requestId,
        "amount": int(total_amount),
        "orderId": orderId,
        "orderInfo": orderInfo,
        "redirectUrl": redirectUrl,
        "ipnUrl": ipnUrl,
        "extraData": extraData,
        "requestType": requestType,
        "signature": signature,
        "lang": lang
    }

    data = json.dumps(data)

    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    return response.json()