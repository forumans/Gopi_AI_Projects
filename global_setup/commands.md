-- Create a Python virtual environment (skip this step,if one already exists)
--python -m venv .venv

-- Activate the virtual environment
.venv\Scripts\activate

--upgrade Pip
python -m pip install --upgrade pip

-- Install required packages
pip install -r libs_required.txt

-- Run the app
streamlit run app.py

-- Deactivate the virtual environment
deactivate

-- Remove the virtual environment
del .venv


