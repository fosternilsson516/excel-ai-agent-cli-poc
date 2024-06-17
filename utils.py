import os
import json
import re
import pandas as pd

def extract_excel_metadata(file_path):
    """Extracts metadata from an Excel file and returns it as a JSON-like string.

    Args:
        file_path (str): The path to the Excel file.
        num_sample_rows (int, optional): Number of sample rows to analyze. Defaults to 2.

    Returns:
        str: A string containing the extracted metadata in a JSON-like format.
    """
    num_sample_rows = 2
    metadata_str = "{"  # Start the JSON string
    metadata_str += f'"file_path": "{file_path}",'

    with pd.ExcelFile(file_path) as xls:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name, nrows=num_sample_rows)
            numeric_columns = df.select_dtypes(include='number').columns

            metadata_str += f'"{sheet_name}": ' + "{"
            metadata_str += f'  "columns": {json.dumps(list(df.columns))}, '
            metadata_str += f'  "data_types": {json.dumps(df.dtypes.astype(str).to_dict())}, '

            # Sample Values (handle Timestamps)
            sample_values = df.head(num_sample_rows).to_dict(orient="list")
            for col, values in sample_values.items():
                if df[col].dtype == "datetime64[ns]":
                    sample_values[col] = [str(v) for v in values]
            metadata_str += f'  "sample_values": {json.dumps(sample_values)}, ' 

            metadata_str += f'  "unique_value_counts": {json.dumps({col: df[col].nunique() for col in df.columns})}, '

            # Numeric Stats
            numeric_stats_str = "{"
            for col in numeric_columns:
                min_val = round(float(df[col].min()), 1) if not pd.isnull(df[col].min()) else "null"
                max_val = round(float(df[col].max()), 1) if not pd.isnull(df[col].max()) else "null"
                mean_val = round(float(df[col].mean()), 1) if not pd.isnull(df[col].mean()) else "null"
                std_val = round(float(df[col].std()), 1) if not pd.isnull(df[col].std()) else "null"
                numeric_stats_str += f'"{col}": ' + "{" + f'"min": {min_val}, "max": {max_val}, "mean": {mean_val}, "std": {std_val}' + "}, "
            numeric_stats_str = numeric_stats_str.rstrip(", ") + "}"  # Remove trailing comma and close the object
            metadata_str += f'  "numeric_stats": {numeric_stats_str}' 

            metadata_str += "}, "  # Close sheet metadata object

    metadata_str = metadata_str.rstrip(", ") + "}"  # Remove trailing comma and close the main object
    return metadata_str  

def extract_data_from_response(json_api_response, file_path):
    """Extracts data from an Excel file based on a JSON response.

    Args:
        response_str (str): The JSON string containing file, sheet, and column information.
        file_path (str): The path to the Excel file.

    Returns:
        pandas.DataFrame or dict: A DataFrame if one sheet, dict of DataFrames if multiple.
    """

    json_api_response = json_api_response.strip().strip("```")
    json_api_response = json_api_response.lstrip("json")

    response_data = json.loads(json_api_response)

    all_data = {}  # Store data from multiple sheets if needed

    # Get actual file name from file_path
    file_name = os.path.basename(file_path)

    with pd.ExcelFile(file_path) as xls:
        for sheet_name in response_data["sheets"][file_name]:  # Iterate over sheets in the file
            columns_to_extract = response_data["columns"][file_name][sheet_name]
            df = pd.read_excel(xls, sheet_name, usecols=columns_to_extract)
            all_data[sheet_name] = df

    if len(all_data) == 1:
        # If only one sheet, return a single DataFrame
        return all_data[next(iter(all_data))]  # Get the single DataFrame value
    else:
        # If multiple sheets, return a dictionary of DataFrames
        return all_data  

def extract_dataframe_metadata(final_df):
    """
    Extracts metadata from a Pandas DataFrame to be used in conjunction with
    natural language prompts for data transformations.

    Args:
        df (pd.DataFrame): The DataFrame to extract metadata from.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """

    metadata = {
        "shape": final_df.shape,  # Number of rows and columns
        "dtypes": final_df.dtypes.to_dict(),  # Datatypes of each column (as a dict)
        "columns": list(final_df.columns),  # List of column names
        "non_null_counts": final_df.count().to_dict(),  # Non-null values per column
        "describe": final_df.describe().to_dict(),  # Summary statistics (if numerical)
        "unique_value_counts": {col: final_df[col].nunique() for col in final_df.columns},  # Unique values per column
        # Add other metadata you might find relevant here
    }

    return metadata

def apply_pandas_script(df, script_text):
    """Executes a Pandas script on a DataFrame and returns the modified DataFrame."""

    # Create a copy of the DataFrame to avoid modifying the original
    modified_df = df.copy()
    script_text = script_text.strip().strip("```")
    script_text = script_text.lstrip("python")

    # Create a dictionary to capture local variables from the script
    local_vars = {}
    local_vars['df'] = modified_df.copy()

    try:
        # Execute the script in the context of the local_vars dictionary
        exec(script_text, globals(), local_vars)
        
        # The modified DataFrame should be stored in the 'df' variable within local_vars
        if "df" in local_vars:
            modified_df = local_vars["df"]
        else:
            raise ValueError("The script did not modify the DataFrame 'df'.")

    except Exception as e:
        print(f"Error executing Pandas script: {e}")
        return df  # Return the original DataFrame in case of error

    return modified_df    