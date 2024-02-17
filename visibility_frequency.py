import csv

# Define the input and output file names
input_file = 'METAR_2014_2023.csv'
output_file = 'visibility_frequency.csv'

# Create a dictionary to store the frequency of visibility values
visibility_frequency = {}

# Open the input CSV file and read data
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    
    # Iterate over each row in the CSV file
    for row in reader:
        # Split the METAR data into a list of components
        metar_components = row['metar'].split()
        
        # Find the component that ends with 'SM' and extract the visibility value
        visibility = None
        for component in metar_components:
            if component.endswith('SM'):
                visibility = component[:-2]  # Exclude 'SM' suffix
                break
        
        # Convert visibility value to decimal if it is in the format '1/2'
        if visibility and '/' in visibility:
            numerator, denominator = map(int, visibility.split('/'))
            visibility = round(numerator / denominator, 2)
        
        # Update the visibility frequency dictionary
        if visibility is not None:
            if visibility in visibility_frequency:
                visibility_frequency[visibility] += 1
            else:
                visibility_frequency[visibility] = 1

# Write the visibility frequency data to a new CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['visibility (SM)', 'frequency'])
    
    # Write each visibility frequency pair to the CSV file
    for visibility, frequency in visibility_frequency.items():
        writer.writerow([visibility, frequency])

print("Output written to", output_file)
