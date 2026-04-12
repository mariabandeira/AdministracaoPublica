# CadUnico Project

This project focuses on analyzing and visualizing data from the Cadastro Único (CadÚnico) program in Brazil, particularly related to the Bolsa Família program. It includes data cleaning, processing, and machine learning model training for various states, including Piauí (PI), Bahia (BA), Ceará (CE), Paraíba (PB), and Rio Grande do Norte (RN).

## Project Structure

- **.env**: Contains environment variables for configuration, such as paths to data files and model files.
- **cadunico_2018.ipynb**: Jupyter notebook for analysis or processing of CadÚnico data for the year 2018.
- **dashboard.py**: Main dashboard application built using Streamlit for visualizing data related to the Bolsa Família program.
- **DataCleaningPB.ipynb**: Jupyter notebook for cleaning and preprocessing data specific to Paraíba (PB).
- **DataCleaningRN.ipynb**: Jupyter notebook for cleaning and preprocessing data specific to Rio Grande do Norte (RN).
- **requirements.txt**: Lists the Python packages required to run the project.

### State-Specific Directories

- **BaesesPI**: Contains data and scripts related to Piauí (PI).
  - `cadunico_pi_clean.csv`: Cleaned dataset for Piauí.
  - `clean_bases_pi.py`: Python script for cleaning raw data for Piauí.
  - `extraindoBases.ipynb`: Jupyter notebook for extracting and processing data for Piauí.
  - **BasesAno**: Annual datasets for Piauí from 2012 to 2018.

- **BasesBA**: Contains data and scripts related to Bahia (BA).
- **BasesCE**: Contains data and scripts related to Ceará (CE).
- **BasesPB**: Contains data and scripts related to Paraíba (PB).
- **BasesRN**: Contains data and scripts related to Rio Grande do Norte (RN).
- **BasesRNPB**: Combined datasets for Paraíba and Rio Grande do Norte from 2012 to 2018.

### Machine Learning Directories

- **KNN**: Jupyter notebooks for training K-Nearest Neighbors models.
- **RandomForest**: Jupyter notebooks for training Random Forest models.
- **RNN**: Jupyter notebooks for training Recurrent Neural Networks.
- **SVM**: Jupyter notebooks for training Support Vector Machine models.
- **XGBoost**: Jupyter notebooks for training XGBoost models.

## Setup Instructions

1. Clone the repository or download the project files.
2. Install the required packages listed in `requirements.txt` using pip:
   ```
   pip install -r requirements.txt
   ```
3. Set up the environment variables in the `.env` file as needed.
4. Run the `dashboard.py` file to start the Streamlit application:
   ```
   streamlit run dashboard.py
   ```

## Usage

- Use the dashboard to visualize data related to the Bolsa Família program.
- Explore the data cleaning notebooks to understand how the datasets are processed.
- Train machine learning models using the provided Jupyter notebooks for different algorithms.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.