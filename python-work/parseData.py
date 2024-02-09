# import sys
# filePath=sys.argv[1]
# print(filePath)


import csv
import os


def generate_datasets_from_csv(csv_file_path):
    merchant_to_pincodes = {}
    pincode_to_merchants = {}

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            merchant_id = int(row['MerchantID'])
            pincodes = [int(row[f'Pincode{i}']) for i in range(1, len(row)) if row[f'Pincode{i}'] != '0']

            # Mapping merchants to pincodes
            merchant_to_pincodes[merchant_id] = pincodes

            # Mapping pincodes to merchants
            for pincode in pincodes:
                if pincode not in pincode_to_merchants:
                    pincode_to_merchants[pincode] = []
                pincode_to_merchants[pincode].append(merchant_id)

    return merchant_to_pincodes, pincode_to_merchants






present_working_directory=os.getcwd()

try:
    csv_file_path = str(present_working_directory+"/uploads/myCSV.csv")
    merchant_to_pincodes, pincode_to_merchants = generate_datasets_from_csv(csv_file_path)

    with open(present_working_directory+'/python-work/parsed_dictionary.py', 'w') as parsed_dictionary:
        parsed_dictionary.write("pincode_to_merchant="+str(pincode_to_merchants))
        parsed_dictionary.write("\n")
        parsed_dictionary.write("merchant_to_pincode="+str(merchant_to_pincodes)) 


    print("Sucessfully created file") 






except Exception as e:
    print(e)
    print("Cannot open file")

