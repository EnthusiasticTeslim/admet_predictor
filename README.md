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
git clone https://github.com/EnthusiasticTeslim/admet_predictor
cd admet_predictor
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

## Future Work

1. Enhance Molecular Visualization:
   - Implement interactive 3D molecular visualization using py3Dmol
   - Add support for different visualization styles (ball-and-stick, surface, etc.)
   - Enable rotation, zoom, and measurement tools
   - Include 2D structure depiction option

2. Improve Prediction Models:
   - Replace placeholder values with RDKit-based descriptors and properties
   - Integrate empirical models for key ADMET properties:
     - LogP and LogS calculations
     - Molecular weight and topological polar surface area
     - Number of rotatable bonds and H-bond donors/acceptors
   - Add machine learning models trained on experimental data
   - Include confidence scores for predictions

3. Current Features:
   - Basic SMILES input and file upload functionality
   - Simple color-coded risk assessment:
     - Green: Favorable/Low risk
     - Yellow: Moderate risk  
     - Red: High risk/Concerning

## Dependencies

- shiny
- shinywidgets
- bslib
- pandas
- numpy

## License

Free for all. No assurance ! 