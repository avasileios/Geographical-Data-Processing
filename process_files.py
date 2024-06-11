""" Antwnopoulos Vasileios Chasapis Christos"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import statsmodels.api as sm
from statsmodels.formula.api import ols
import os
import logging
from tqdm import tqdm

# Logging
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define the directories
dir = r'D:\Uth\Master Cs\2nd Semester\Συστήματα Γεωγραφικών Πληροφοριών\geografika\Project2'
country = r'\Βοζνία'  # Σερβία, Κροατία και Βοζνία
output_folder_name = r'\results'

input_dir = dir + country
output_base_dir = input_dir + output_folder_name

# Ensure the output directory exists
os.makedirs(output_base_dir, exist_ok=True)

# List to hold summary report data
summary_report = []

def read_and_clean_data(file_path):
    columns = ['Year', 'Month', 'Day', 'Value']
    df = pd.read_csv(file_path, delimiter=';', skiprows=1, names=columns)
    # Keep only relevant columns
    df = df[['Year', 'Month', 'Day', 'Value']]
    # Replace invalid data (-9999) with NaN and drop rows with NaN values
    df['Value'] = df['Value'].replace(-9999, pd.NA)
    return df.dropna(subset=['Value'])

def save_grouped_data(df, output_dir):
    # Group by 'Year' and 'Month' and calculate the mean of 'Value'
    df1 = df.groupby(['Year', 'Month'])['Value'].mean().reset_index()
    df1.to_csv(os.path.join(output_dir, 'mm.csv'), index=False, sep=';')
    # Group by 'Month' and calculate the mean of 'Value'
    df2 = df.groupby('Month')['Value'].mean().reset_index()
    df2.to_csv(os.path.join(output_dir, 'ovmm.csv'), index=False, sep=';')
    return df1, df2

def merge_and_save_data(df1, df2, output_dir):
    # Merge the two DataFrames on 'Month'
    merged_df = pd.merge(df1, df2, on='Month', suffixes=('_mm', '_ovmm'))
    merged_df = merged_df[['Year', 'Month', 'Value_mm', 'Value_ovmm']]
    merged_df = merged_df.sort_values(by=['Year', 'Month'])
    # Calculate the difference between 'Value_mm' and 'Value_ovmm'
    merged_df['desmm'] = merged_df['Value_mm'] - merged_df['Value_ovmm']
    merged_df['desmm'] = merged_df['desmm'].astype(float)
    # Add a numeric index column
    merged_df.reset_index(drop=True, inplace=True)
    merged_df['numeric_index'] = merged_df.index
    merged_df.to_csv(os.path.join(output_dir, 'merged.csv'), index=False, sep=';')
    return merged_df

def plot_data(df2, output_dir, file_name):
    """Plot average monthly values."""
    plt.figure(figsize=(10, 6))
    plt.plot(df2['Month'], df2['Value'], marker='o', linestyle='-')
    plt.title(f'Average Monthly Value (ovmm) - {file_name}')
    plt.xlabel('Month')
    plt.ylabel('Value')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'{file_name}_average_monthly_values.png'), metadata={'Title': f'Average Monthly Value (ovmm) - {file_name}'})
    plt.close()

def plot_desmm_timeline(merged_df, output_dir, file_name):
    """Plot the time series of 'desmm'."""
    plt.figure(figsize=(10, 6))
    plt.plot(merged_df['numeric_index'], merged_df['desmm'], marker='o', linestyle='-')
    plt.title(f'Desmm Timeline - {file_name}')
    plt.xlabel('Index')
    plt.ylabel('Desmm')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'{file_name}_desmm_timeline.png'), metadata={'Title': f'Desmm Timeline - {file_name}'})
    plt.close()

def plot_regression(merged_df, output_dir, file_name):
    """Plot scatter with regression line and return regression statistics."""
    index_numeric = merged_df['numeric_index'].to_numpy(dtype=float)
    desmm_numeric = merged_df['desmm'].to_numpy(dtype=float)

    # Calculate linear regression
    slope, intercept, r_value, p_value, std_err = linregress(index_numeric, desmm_numeric)
    regression_line = slope * index_numeric + intercept

    plt.figure(figsize=(10, 6))
    plt.scatter(index_numeric, desmm_numeric, color='red', label='Scatter Plot')
    plt.plot(index_numeric, regression_line, color='blue', label='Linear Regression Line')
    plt.title(f'Desmm Timeline Scatter with Regression Line - {file_name}')
    plt.xlabel('Index')
    plt.ylabel('Desmm')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{file_name}_scatter_with_regression_line.png'), metadata={'Title': f'Desmm Timeline Scatter with Regression Line - {file_name}'})
    plt.close()

    return slope, intercept, r_value, p_value, std_err

def perform_ols(merged_df, output_dir, file_name):
    """Perform OLS regression and save regression statistics and ANOVA table."""
    model = ols('desmm ~ numeric_index', data=merged_df).fit()
    anova_table = sm.stats.anova_lm(model)

    with open(os.path.join(output_dir, f'{file_name}_regression_and_anova.txt'), 'w') as f:
        f.write(f"File: {file_name}\n\n")
        f.write("Regression Statistics:\n")
        f.write(model.summary().as_text())
        f.write("\n\nANOVA Table:\n")
        f.write(anova_table.to_string())

    return model

def process_file(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(output_base_dir, file_name)
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = read_and_clean_data(file_path)
        df1, df2 = save_grouped_data(df, output_dir)
        plot_data(df2, output_dir, file_name)
        merged_df = merge_and_save_data(df1, df2, output_dir)
        plot_desmm_timeline(merged_df, output_dir, file_name)
        slope, intercept, r_value, p_value, std_err = plot_regression(merged_df, output_dir, file_name)
        perform_ols(merged_df, output_dir, file_name)

        # Append summary statistics to the report
        summary_report.append({
            'File': file_name,
            'Slope': slope,
            'Intercept': intercept,
            'R-squared': r_value**2,
            'P-value': p_value,
            'Standard Error': std_err
        })

        logging.info(f"Successfully processed {file_name}")

    except Exception as e:
        logging.error(f"Error processing {file_name}: {e}")
        print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    # Get list of all CSV files in the input directory
    files = [file for file in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, file)) and file.endswith('.csv')]
    for file_name in tqdm(files, desc="Processing files"):
        file_path = os.path.join(input_dir, file_name)
        process_file(file_path)

    summary_df = pd.DataFrame(summary_report)
    summary_df.to_csv(os.path.join(output_base_dir, 'summary_report.csv'), sep=';', index=False)

    print("Processing complete. Summary report saved to summary_report.csv")