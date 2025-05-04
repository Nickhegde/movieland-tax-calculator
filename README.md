# Movieland Tax Program

This README provides instructions on how to execute the `movieland_tax.py` program and outlines the assumptions and approach used in its implementation.

---

## How to Execute

1. **Ensure Python is Installed**  
    Make sure you have Python 3.x installed on your system.

2. **Navigate to the Program Directory**  
    Open a terminal and navigate to the directory containing `movieland_tax.py`.

3. **Run the Program**  
    Execute the program by providing the file path to the input data as a command-line argument:  
    ```bash
    python movieland_tax.py <path_to_income_file> <path_to_panels_file> > result.json
    ```
    Replace `<path_to_income_file>` with the actual path to the input file containing income data and `<path_to_panels_file>` with the actual path to the input file containing panels data.

---

## Assumptions

1. **Tax Year**  
    The program calculates tax only for the year **2024**.

2. **Taxable Income Threshold**  
    If the taxable income exceeds **$90,000**, the panel count cap is removed from the credits calculation.

3. **Panel ID Format**  
    Panel IDs are assumed to follow a consistent format and are unique.

4. **Data Cleaning**  
    The program removes null values and empty rows from the input data before processing.

---

## Approach

1. **Reading Input File**  
    The program starts by reading the file path provided via the command line. It loads the panel data from the specified file.

2. **Counting Panels**  
    The total count of panels is calculated from the input data.

3. **Generating Tax Brackets**  
    Tax brackets for **2024** are generated based on the **2023** brackets, with necessary adjustments.

4. **Data Cleaning**  
    The income data is sorted, and null values or empty rows are removed to ensure accurate calculations.

5. **Tax Calculation**  
    Taxes are calculated for both the month and the year based on the specified conditions, including the taxable income threshold.

---

Feel free to reach out if you encounter any issues or have questions about the program.  