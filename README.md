echo "# London Property Investment Analysis

A Python-based analysis tool for residential property investments in London, focusing on mortgages and rental returns.

## Features
- Mortgage payment calculations with different LTV ratios
- Interest rate analysis based on LTV
- Rental yield analysis for London Zones 1 & 2
- Total ROI analysis including:
  - Cash returns from rental income
  - Equity buildup through mortgage amortization
  - Property appreciation scenarios

## Project Structure
\`\`\`
mortgage-analysis/
├── notebooks/
│   ├── 01_basic_mortgage_calculator.ipynb
│   ├── 02_ltv_analysis.ipynb
│   └── 03_rental_roi_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── mortgage_calculator.py
│   └── rental_analysis.py
└── requirements.txt
\`\`\`

## Setup
1. Create a virtual environment:
\`\`\`
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. Install requirements:
\`\`\`
pip install -r requirements.txt
\`\`\`

3. Launch Jupyter:
\`\`\`
jupyter notebook
\`\`\`

## Usage
1. Start with \`01_basic_mortgage_calculator.ipynb\` for basic mortgage calculations
2. Explore \`02_ltv_analysis.ipynb\` for LTV impact analysis
3. Use \`03_rental_roi_analysis.ipynb\` for complete investment analysis

## Assumptions
- Interest rates based on current UK mortgage market
- Rental yields:
  - Zone 1: 2.8% - 4.2%
  - Zone 2: 3.3% - 4.8%
- Property appreciation: 2% - 6.5% per annum
