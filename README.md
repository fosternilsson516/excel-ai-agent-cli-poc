## Excel AI Assistant: A Chat-Based CLI for Excel Data Manipulation

This command-line interface (CLI) tool leverages the power of large language models (LLMs) to streamline the manipulation of your Excel data. It's designed to be intuitive and user-friendly, allowing you to interact with your spreadsheets using natural language queries, similar to how you'd communicate with another person.

### Features

- **Chat-Like Interface:** Pose questions or requests in plain English.
- **Step-by-Step Guidance:** The tool suggests actions to take based on your query.
- **Pandas Code Generation:**  Enter "g" (for generate) to get a custom Pandas script to perform the suggested actions.
- **Safe, Local Execution:** The Pandas script runs within your environment, keeping your data private and secure.
- **Metadata-Driven Prompts:**  The tool intelligently extracts metadata from your Excel file to create concise and effective prompts for the LLM, resulting in efficient interactions.

### How It Works

1. **File Path Input:** You'll be prompted to enter the full path to your Excel file.
2. **Query Input:**  Describe what you want to do with your data (e.g., "Calculate the average sales for each region").
3. **Suggested Steps:** The tool will provide a series of steps it thinks are necessary to fulfill your request.
4. **Generate Pandas Script:** If you're satisfied with the steps, type "g" and the tool will generate a Pandas script tailored to your query.
5. **Local Execution:** The generated script runs within your Python environment, manipulating your Excel data directly.

### Installation and Setup

1. **Prerequisites:**
   - Python (3.x recommended)
   - Gemini API key (sign up for free tokens)

2. **Clone Repository:**
   ```bash
   git clone [https://github.com/your_username/excel-agents-bot.git](https://github.com/your_username/excel-agents-bot.git) 

3.  **Virtual Environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    Use code with caution.
    ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    Use code with caution.
    ```

5.  **Set Up Environment Variables:**
    -   Create a `.env` file in the project root directory with the following:

    ```
    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_ENDPOINT=gemini-1.5-flash
    ```

### Usage

1.  **Activate Environment:**

    ```bash
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    Use code with caution.
    ```

2.  **Run the CLI:**

    ```bash
    python app.py
    Use code with caution.
    ```

### Future Plans

Excel Integration: Use openpyxl or xlwings to directly write results back to the original Excel file or enable real-time manipulation.
File Format Expansion: Integrate Apache Tika to support a wider range of file types for metadata extraction.

### Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or share your ideas for improvement.

### Disclaimer

This project is a prototype and should not be used for sensitive or critical data operations without thorough testing.

---

**Author:** Your Name

**License:** GNU General Public License v3.0 (GPLv3)   
