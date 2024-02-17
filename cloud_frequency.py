import csv

# Define the input and output file names
input_file = 'METAR_2014_2023.csv'
output_file = 'cloud_frequency.csv'

# Define the cloud codes
cloud_codes = ['FEW', 'SCT', 'BKN', 'OVC', 'NSC', 'SKC', 'NCD', 'CLR']

# Create a dictionary to store the frequency of cloud types
cloud_frequency = {code: 0 for code in cloud_codes}

# Open the input CSV file and read data
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in reader:
        # Extract the METAR data
        metar = row['metar']
        
        # Check for each cloud code in the METAR data
        for code in cloud_codes:
            if code in metar:
                cloud_frequency[code] += 1

# Write the cloud frequency data to a new CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['clouds', 'frequency'])
    
    # Write each cloud frequency pair to the CSV file
    for code, frequency in cloud_frequency.items():
        writer.writerow([code, frequency])

print("Output written to", output_file)
