import pandas as pd
import re

def reorder_formula(formula):
    # Parse the formula to extract elements and counts
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    
    # Sort elements based on count
    sorted_elements = sorted(elements, key=lambda x: int(x[1]) if x[1] else 1, reverse=False)
    
    # Reconstruct the reordered formula
    reordered_formula = ''.join([f"{element[0]}{element[1]}" for element in sorted_elements])
    
    return reordered_formula, sorted_elements

# Read Excel file
input_file = "formulae.xlsx"  # Change this to your input file name
output_file = "output_smallest_largest.xlsx"  # Change this to your desired output file name

df = pd.read_excel(input_file)

# Reorder chemical formulae and extract elements
df['Reordered_Formula'], df['Elements'] = zip(*df['Chemical_Formula'].apply(reorder_formula))

# Expand elements into separate columns
elements_df = df['Elements'].apply(pd.Series)
elements_df.columns = [f"Element_{i+1}" for i in range(elements_df.shape[1])]

# Replace empty strings with "1" for cases where there is only one of an element
elements_df = elements_df.replace("", '1')

# Concatenate the original DataFrame with the elements DataFrame
df = pd.concat([df, elements_df], axis=1)

# Write to output file
df.to_excel(output_file, index=False)

print("Reordering completed. Output file created:", output_file)
