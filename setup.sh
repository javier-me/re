# First, let's create the basic files
echo "# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
ENV/

# Jupyter
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db" > .gitignore

echo "numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
jupyter==1.0.0
ipywidgets==8.0.7" > requirements.txt
# Could not install with pip install -r requirements.txt so had to type package names mannually in pip without version numbers