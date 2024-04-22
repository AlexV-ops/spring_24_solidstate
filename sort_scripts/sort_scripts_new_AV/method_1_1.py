import pandas as pd
import re

# Function to parse chemical formulas with fractional counts
def parse_formula(formula):
    elements = re.findall('([A-Z][a-z]*)(\d*\.?\d*)', formula)
    counts = {}
    for element, count in elements:
        count = float(count) if count else 1
        if count == int(count):  # Check if count is a whole number
            count = int(count)  # Convert to integer if whole number
        counts[element] = count
    return counts

# Function to reorder the formula based on element counts
def reorder_formula(parsed_formula):
    sorted_elements = sorted(parsed_formula.items(), key=lambda x: (-x[1], x[0]))
    reordered_elements = [(elem, '') if count == 1 else (elem, count) for elem, count in sorted_elements]
    reordered_formula = ''.join([f"{elem}{count}" for elem, count in reordered_elements])
    return reordered_formula, reordered_elements

# Read the Excel file
df = pd.read_excel('formulae.xlsx', sheet_name='Samples')

# Initialize lists to store data
new_data = []

# Iterate over each row
for idx, row in df.iterrows():
    formula = row['Chemical_Formula']
    parsed_formula = parse_formula(formula)
    reordered_formula, reordered_elements = reorder_formula(parsed_formula)
    elements = [elem for elem, _ in reordered_elements]
    counts = [count for _, count in reordered_elements]
    
    # Create data for the new DataFrame
    new_row = {'Formula': formula, 'Reordered_Formula': reordered_formula}
    
    # Add columns for each element and its count
    for i in range(len(elements)):
        new_row[f'Element_{i+1}'] = elements[i]
        new_row[f'Index_{i+1}'] = counts[i] if counts[i] != '' else 1
    
    new_data.append(new_row)

# Create a new DataFrame
new_df = pd.DataFrame(new_data)

# Write the new DataFrame to Excel
new_df.to_excel('output_1_1.xlsx', index=False)
