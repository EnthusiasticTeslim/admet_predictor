# ADMET Prediction Web Application

A responsive web application for predicting ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties of chemical compounds using Python Shiny.

## Features

- SMILES string input and file upload support
- Real-time ADMET property predictions
- Responsive design for both desktop and mobile
- Color-coded prediction results
- Visual metrics dashboard showing:
  - Total properties analyzed
  - Number of predictions made
  - Number of conditions passed/failed
  - Warning indicators for concerning predictions

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd admet-modeling
```

2. Environment setup (recommended):

```bash
~$chmod +x setup.sh
~$sh setup.sh
~$source admet/bin/activate
```


## Usage

1. Start the application:
```bash
shiny run --reload app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8000)

3. Enter a SMILES string or upload a SMILES file (.smi or .txt)

4. View the predicted ADMET properties

## Dependencies

- shiny
- shinywidgets
- bslib
- pandas
- numpy

## License

Free for all. No assurance ! 