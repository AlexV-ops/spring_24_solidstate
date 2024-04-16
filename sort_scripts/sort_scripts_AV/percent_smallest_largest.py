import pandas as pd
import re

def reorder_formula(formula):
    # Parse the formula to extract elements and counts
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    
    # Calculate total count of atoms
    total_count = sum(int(count) if count else 1 for _, count in elements)
    
    # Calculate atomic percentages for each element
    atomic_percentages = {element: (int(count) if count else 1) / total_count * 100 for element, count in elements}
    
    # Sort elements based on atomic percentages
    sorted_elements = sorted(atomic_percentages.items(), key=lambda x: x[1], reverse=False)
    
    # Reconstruct the reordered formula
    reordered_formula = ', '.join([f"{int(percentage)}% {element}" for element, percentage in sorted_elements])
    
    return reordered_formula

# Read Excel file
input_file = "formulae.xlsx"  # Change this to your input file name
output_file = "output_percent_smallest_largest.xlsx"  # Change this to your desired output file name

df = pd.read_excel(input_file)

# Reorder chemical formulae
df['Reordered_Formula'] = df['Chemical_Formula'].apply(reorder_formula)

# Write to output file
df.to_excel(output_file, index=False)

print("Reordering completed. Output file created:", output_file)
