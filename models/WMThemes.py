import pandas as pd

# Load your dataset
df = pd.read_csv('final.csv')

# Define the theme names and corresponding column names in the DataFrame
theme_columns = {
    'AI/ Machine Learning': 'AI/ML', 
    'Customer Centricity': 'CC', 
    'Data & Analytics': 'DA', 
    'Digital Transformation': 'DT',
    'Human-centered design': 'HCD', 
    'Innovation': 'I', 
    'Organizational Change Management': 'OCM', 
    'Product Development': 'PD',
    'Research & Development': 'RD', 
    'Transactions': 'T', 
    'User Experience': 'UX'
}

# Create a new column 'Themes' and initialize with an empty list
df['Themes'] = ''

# Iterate over each row
for index, row in df.iterrows():
    # List to store themes where the corresponding column is 1
    row_themes = []
    
    # Iterate over the theme_columns dictionary
    for theme, col_name in theme_columns.items():
        if row[col_name] == 1:
            row_themes.append(theme)
    
    # If no themes are found, assign 'MISC'
    if not row_themes:
        df.at[index, 'Themes'] = 'MISC'
    else:
        # Join the list of themes into a comma-separated string
        df.at[index, 'Themes'] = ', '.join(row_themes)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_file.csv', index=False)

print("Processing complete. Check 'updated_file.csv' for the results.")
