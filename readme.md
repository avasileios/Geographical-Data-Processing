# 🌍 Geographical Data Processing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Data](https://img.shields.io/badge/Data-Geographical-orange?style=for-the-badge&logo=databricks)

This project processes **geographical data from CSV files**.  
It reads the data, performs various analyses, generates plots, and saves the results for further exploration.  

---

## 📂 Project Structure

- `process_files.py` – Main script for processing CSV files.  
- `Interpolation_using_griddata.py` – Script for plotting Griddata Interpolation.  
- `processing.log` – Log file containing processing details and errors.  
- `requirements.txt` – List of dependencies.  

---

## ⚙️ Setup

### 🔑 Prerequisites
- Python **3.x**  

### 📦 Installation
Install the required packages:
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### 1️⃣ Prepare Input Files
Place your CSV files in the **input directory** specified in the script.  
Modify the `input_dir` and `output_base_dir` in `process_files.py` according to your directory structure.  

### 2️⃣ Run the Script
```bash
python process_files.py
```

### 3️⃣ Output
- Processed CSV files  
- Plots and analysis results  
- `summary_report.csv` (summary report of all results)  

All outputs will be saved in the specified output directory.  

---

## 📦 Dependencies
- `pandas`  
- `matplotlib`  
- `scipy`  
- `statsmodels`  
- `tqdm`  

---

## 📝 Logging
A `processing.log` file is generated to log **all processing details and errors**.  

---

## 📁 Directory Structure

Expected structure:
```
project-directory
├── README.md
├── requirements.txt
├── process_files.py
└── processing.log
```

### Example structure with input files:
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

Processed results will be saved in the `results` folder within each respective country folder.  

---

## 🤝 Contributing
Contributions are welcome!  
Fork this repository, make your improvements, and submit a pull request.  

---

## 📜 License
This project is licensed under the **MIT License**.  
