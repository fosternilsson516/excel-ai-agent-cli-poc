from flask import Flask, render_template, request, jsonify
from gemini_api_caller import promptAPICaller
from config import Config
from utils import extract_excel_metadata, extract_data_from_response, extract_dataframe_metadata, apply_pandas_script
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Initialize classes (you can do this globally or within a request context)
config = Config()
prompt_api_caller = promptAPICaller()

final_df = None
full_metadata = None
steps_api_response = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global final_df, full_metadata, steps_api_response
    message = request.form.get('message')
    file = request.files.get('file')
    file_path = None
    print(file)

    if file:
        filename = secure_filename(file.filename)
        file.save(filename)  # Save the file if needed (adjust the path as necessary)
        file_path = file.filename
        print(file_path)
        full_metadata = extract_excel_metadata(file_path)

    if message.lower() == "g" and final_df is not None and not final_df.empty:
        # Generate and Execute Pandas Script
        prompt3 = prompt_api_caller.create_prompt(steps_api_response, config.get_prompt_prefix("code_writer"), final_metadata)
        pandas_script_api_response = prompt_api_caller.call_gemini_api(prompt3)
        result_df = apply_pandas_script(final_df, pandas_script_api_response)
        response_text = f"Pandas Script:\n{pandas_script_api_response}\n\nResult:\n{result_df.to_markdown(index=False, numalign='left', stralign='left')}"

    elif file_path is None:
        response_text = "Please upload an Excel file first."       
    else:
        # Process Query
        query = message
        prompt1 = prompt_api_caller.create_prompt(query, config.get_prompt_prefix("extract_json_data"), full_metadata)
        json_api_response = prompt_api_caller.call_gemini_api(prompt1)
        final_df = extract_data_from_response(json_api_response, file_path)
        final_metadata = extract_dataframe_metadata(final_df)
        prompt2 = prompt_api_caller.create_prompt(query, config.get_prompt_prefix("generate_steps"), final_metadata)
        steps_api_response = prompt_api_caller.call_gemini_api(prompt2)
        response_text = steps_api_response    
    
    response = {
        "response": response_text,  # Your LLM's response here
    }
    return jsonify(response)