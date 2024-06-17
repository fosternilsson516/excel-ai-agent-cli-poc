from config import Config
from gemini_api_caller import promptAPICaller
from utils import extract_excel_metadata, extract_data_from_response, extract_dataframe_metadata, apply_pandas_script

if __name__ == "__main__":

    config = Config()
    prompt_api_caller = promptAPICaller()
    while True:
        file_path = input("Enter The excel file path (or type 'q' to quit): ")
        if file_path.lower() == "q":
            break
        try:
            full_metadata = extract_excel_metadata(file_path)  # Check if valid file path
            break  # Exit loop if valid
        except FileNotFoundError:
            print("Invalid file path. Please try again.")  
    final_df = None
    while True:
        try:                          
            user_input = input("Enter your query (type 'q' to quit or 'g' to generate and continue): ")
            if user_input.lower() == "q":
                break
            elif user_input.lower() == "g" and final_df is not None and not final_df.empty:
                prompt3 = prompt_api_caller.create_prompt(steps_api_response, config.get_prompt_prefix("code_writer"), final_metadata)
                pandas_script_api_response = prompt_api_caller.call_gemini_api(prompt3)
                print(pandas_script_api_response)
                result_df = apply_pandas_script(final_df, pandas_script_api_response)
                print(result_df)
                print("original df:", final_df)
            else:
                query = user_input
                prompt1 = prompt_api_caller.create_prompt(query, config.get_prompt_prefix("extract_json_data"), full_metadata)
                json_api_response = prompt_api_caller.call_gemini_api(prompt1)
                final_df = extract_data_from_response(json_api_response, file_path)
                final_metadata = extract_dataframe_metadata(final_df)
                prompt2 = prompt_api_caller.create_prompt(query, config.get_prompt_prefix("generate_steps"), final_metadata)
                steps_api_response = prompt_api_caller.call_gemini_api(prompt2)
                print(steps_api_response)

        except Exception as e:  # Catching general errors
            print(f"An error occurred: {e}")    

    # ... use data, special_var, and config in your main logic ...
    ##Show me all of the countries that had a profit more than 1 million $ in 2013
    ##Financial Sample.xlsx