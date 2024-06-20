# Geographical Data Processing

This project processes geographical data from CSV files. It reads the data, performs various analyses, generates plots, and saves the results.

## Project Structure

- `process_files.py`: The main script that processes the CSV files.
- `Interpolation_using_griddata.py`: The main script that plots Griddata Interpolation.
- `processing.log`: Log file for processing details and errors.
- `requirements.txt`: List of dependencies.




## Setup

### Prerequisites

- Python 3.x

### Installation


1. **Install the required packages:**

   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Place your CSV files in the input directory specified in the script:**

   Modify the `input_dir` and `output_base_dir` in the `process_files.py` script according to your directory structure.

2. **Run the script:**

   ```
   python process_files.py
   ```

3. **Output:**

   - The processed CSV files, plots, and analysis results will be saved in the specified output directory.
   - A summary report will be saved as `summary_report.csv`.

## Dependencies

- pandas
- matplotlib
- scipy
- statsmodels
- tqdm

## Logging

A `processing.log` file is generated to log the details of the processing and any errors encountered.

## Directory Structure

The expected directory structure is:

```
project-directory
├── README.md
├── requirements.txt
├── process_files.py
└── processing.log
```

## Example Directory Structure

Before running the script, ensure your directory structure looks like this:

```
project-directory/
├── README.md
├── requirements.txt
├── process_files.py
├── Σερβία/
│   ├── file1.csv
│   ├── file2.csv
│   └── ...
├── .../
│   ├── file1.csv
│   ├── file2.csv
│   └── ...
└── processing.log
```

The processed results will be saved in the `results` folder within the respective country folder.

## Contributing

Feel free to fork this repository and make improvements. Pull requests are welcome.

## License

This project is licensed under the MIT License.
