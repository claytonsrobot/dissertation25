filenames = ["canada.csv","new_zealand.csv","united_states.csv"]
df_dict = dict()
    for filename in filenames:
        df_dict = function_to_generate_df_for_each_file_and_add_it_to_df_dict(filename,df_dict)

def function_to_generate_df_for_each_file_and_add_it_to_df_dict(filename,df_dict):
    df = import_from_filename(filename)
    df_dict[filename]=df
    return df_dict
def import_from_filename(filename):
    "stuff"
    return df

## ^^Don't do this
## instead, add all files to the same df, with a filename column


for i,key in enumerate(df.keys()):
    # i is the integer of the filename
    filename = filenames[i]
