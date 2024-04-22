import pandas as pd
from collections import Counter
import re

# Function to parse chemical formulas
def parse_formula(formula):
    elements = re.findall('([A-Z][a-z]*)(\d*)', formula)
    counts = Counter()
    for element, count in elements:
        counts[element] += int(count) if count else 1
    return counts

# Function to reorder the formula based on element counts and Mendeleev number
def reorder_formula(parsed_formula, element_properties):
    sorted_elements = sorted(parsed_formula.items(), key=lambda x: (x[1], element_properties.get(x[0], {}).get('Mendeleev_number', 0), x[0]))
    reordered_formula = ''.join([f"{elem}{count}" for elem, count in sorted_elements])
    return reordered_formula, sorted_elements

# Read the Excel files for chemical formulas and element properties
df_formulas = pd.read_excel('formulae.xlsx', sheet_name='Samples')
df_properties = pd.read_excel('element_properties_for_ML.xlsx')

# Create a dictionary to map element symbols to their Mendeleev numbers
element_properties = df_properties.set_index('Symbol').to_dict('index')

# Initialize lists to store data
new_data = []

# Iterate over each row in the formulas DataFrame
for idx, row in df_formulas.iterrows():
    formula = row['Chemical_Formula']
    parsed_formula = parse_formula(formula)
    reordered_formula, reordered_elements = reorder_formula(parsed_formula, element_properties)
    elements = [elem for elem, _ in reordered_elements]
    counts = [count for _, count in reordered_elements]
    
    # Create data for the new DataFrame
    new_row = {'Formula': formula, 'Reordered_Formula': reordered_formula}
    
    # Add columns for each element and its count
    for i in range(len(elements)):
        new_row[f'Element_{i+1}'] = elements[i]
        new_row[f'Index_{i+1}'] = counts[i]
    
    new_data.append(new_row)

# Create a new DataFrame
new_df = pd.DataFrame(new_data)

# Write the new DataFrame to Excel
new_df.to_excel('output.xlsx', index=False)
