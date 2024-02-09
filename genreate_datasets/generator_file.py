import csv
import random
import os

def generate_random_dataset(num_merchants, max_pincodes_per_merchant):
    dataset = []

    for merchant_id in range(1, num_merchants + 1):
        num_pincodes = random.randint(0, max_pincodes_per_merchant)
        pincodes = random.sample(range(100000, 999999), num_pincodes)  # 6-digit pin codes

        merchant_data = [merchant_id] + pincodes
        dataset.append(merchant_data)

    # Find the maximum number of pincodes among all merchants
    max_pincodes = max(len(merchant_data) - 1 for merchant_data in dataset)

    # Fill in missing pincodes with a placeholder (e.g., 0)
    for merchant_data in dataset:
        merchant_data.extend([0] * (max_pincodes - len(merchant_data) + 1))

    return dataset

def save_dataset_to_csv(dataset, file_path):
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        header = ['MerchantID'] + [f'Pincode{i}' for i in range(1, len(dataset[0]))]
        csv_writer.writerow(header)
        csv_writer.writerows(dataset)

# Example usage:
num_merchants = 100  # 10 million merchants
max_pincodes_per_merchant = 5  # Maximum pincodes per merchant (change as needed)

generated_dataset = generate_random_dataset(num_merchants, max_pincodes_per_merchant)

current_directory = os.getcwd()
output_csv_path = os.path.join(current_directory, 'generated_dataset.csv')

save_dataset_to_csv(generated_dataset, output_csv_path)

print(f'Dataset generated and saved to {output_csv_path}')
