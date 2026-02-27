# Create a Python virtual environment (skip this step,if one already exists)
# python -m venv .venv

# To create a virtual environment with a specific python version such as 3.11
# py -3.11 -m venv .venv311

# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Upgrade Pip
python -m pip install --upgrade pip

# Install required packages
pip install -r libs_required.txt

# Run the app
streamlit run app.py

# Deactivate the virtual environment
deactivate

# Remove the virtual environment
del .venv

# Check pip libraries installed
# All libraries
pip list
# Specific libraries
pip list | Select-String "crewai", "yfinance"
# or alternatively
pip list | findstr "crewai yfinance"

# To create a crew project structure (https://pypi.org/project/crewai/)
crewai create crew <project_name>

