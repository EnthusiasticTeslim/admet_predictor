def get_risk_class(value):
    """Determine the risk class for a given value."""
    if isinstance(value, str):
        if value in ['High', 'Yes', 'Positive']:
            return 'high-risk'
        elif value in ['Medium', 'Moderate']:
            return 'medium-risk'
        else:
            return 'low-risk'
    elif isinstance(value, (int, float)):
        # Handle numeric values
        if isinstance(value, int):
            if value > 1:
                return 'high-risk'
            elif value == 1:
                return 'medium-risk'
            else:
                return 'low-risk'
        else:
            if value > 0.7:
                return 'high-risk'
            elif value > 0.3:
                return 'medium-risk'
            else:
                return 'low-risk'
    return 'low-risk'

def read_smiles(file_content):
    """Read SMILES string from uploaded file."""
    if file_content is not None:
        content = file_content[0]['datapath']
        with open(content, 'r') as f:
            return f.readline().strip()
    return None

def format_value(value):
    """Format numeric values for display."""
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value) 