
import pandas as pd
import os
def df_from_csv_list(filenames):
    combined_df = pd.DataFrame()
    for filepath in filenames:
        # Import data from the CSV file
        temp_df = pd.read_csv(filepath)
        
        # Add filename and filepath columns
        temp_df['filename'] = os.path.basename(filepath)
        temp_df['filepath'] = filepath
        
        # Append to the combined DataFrame
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
    return combined_df

def process_each_filepath(df):
    for index, row in df.iterrows():
        filepath = row['filepath']  # Access the filepath column
        # Perform your action for each filepath
        #print(f"Processing file: {filepath}")
        process_function(filepath)
        
def process_function(filepath):
    print(f"Filepath is Accessed: {filepath}")


if __name__ == "__main__":

    
    filenames = [
        "C:\\me\\canada.csv",
        "C:\\me\\new_zealand.csv",
        "C:\\me\\united_states.csv"
        ]
    
    combined_df = df_from_csv_list(filenames)
    # Your combined DataFrame is ready
    print(combined_df)
    process_each_filepath(combined_df)

    
