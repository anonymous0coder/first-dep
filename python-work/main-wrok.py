from parsed_dictionary import pincode_to_merchant
from parsed_dictionary import merchant_to_pincode
import sys


def merchants_data_retrieval(merchant_id):
    return merchant_to_pincode[merchant_id]

def pincode_data_retrieval(pincode):
    return pincode_to_merchant[pincode]

type=sys.argv[1]
id_to_look=int(sys.argv[2])

try:
    sendData="Not found"
    if type=="merchant":
        sendData=merchants_data_retrieval(id_to_look)
    else:
        sendData=pincode_data_retrieval(id_to_look)
    print(sendData)
except Exception as e:
    print("Data not found")

# print("HEELO")