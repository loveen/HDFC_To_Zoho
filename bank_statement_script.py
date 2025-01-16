import pandas as pd

def transform_bank_statement(input_file, output_file):
    """
    Transforms bank statement data from the given format to the desired format.

    Args:
        input_file: Path to the input CSV file.
        output_file: Path to the output CSV file.
    """

    try:
        # Read the input CSV file
        df = pd.read_csv(input_file)

        # Rename columns for clarity (Note: 'Narration' is used instead of 'Description')
        df = df.rename(columns={
            '  Date     ': 'Date', 
            'Narration                                                                                                                ': 'Description', 
            'Value Dat': 'Value_Dat', 
            'Debit Amount       ': 'Withdrawals',
            'Credit Amount      ': 'Deposits',
            'Chq/Ref Number   ': 'Reference Number',
            'Closing Balance': 'Closing_Balance' 
        })

        # Print column names to verify (for debugging)
        print(df.columns) 

        # Clean the 'Date' column by removing leading/trailing spaces
        df['Date'] = df['Date'].str.strip() 

        # Create a new 'Payee' column 
        df['Payee'] = df['Description'].str.split('-').str[2] 

        # Handle potential errors (e.g., missing values or incorrect split)
        df['Payee'] = df['Payee'].fillna(df['Description']).str.strip() 

        # Format the 'Date' column
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d')

        df['Description'] = df['Description'].str.strip()

        # Select and reorder columns
        df = df[['Date', 'Withdrawals', 'Deposits', 'Payee', 'Description', 'Reference Number']]

        # Fill missing values (if any)
        df = df.fillna('') 

        # Write the transformed data to the output CSV file
        df.to_csv(output_file, index=False)

        print(f"Bank statement transformed successfully. Output saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = 'Acct_Statement_XX8627_16012025.csv'
output_file = 'zoho_statement.csv'
transform_bank_statement(input_file, output_file)