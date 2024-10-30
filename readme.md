# Benefits Cost Optimization and Financial Forecasting Dashboard

## Overview
This project implements a dynamic dashboard for forecasting employee benefits costs and simulating the financial impact of benefits plan adjustments. The dashboard provides interactive visualizations and analysis tools to help benefits analysts make data-driven decisions about employee benefits packages.

## Features
- Interactive cost forecasting using Facebook Prophet
- Benefits cost distribution analysis
- Cost drivers visualization
- ROI calculation and analysis
- What-if scenario planning for benefit adjustments
- Data quality monitoring

## Dataset
The project uses the Medical Cost Personal Dataset from Kaggle, which includes the following features:
- age: Age of primary beneficiary
- sex: Gender of insurance contractor 
- bmi: Body mass index
- children: Number of children covered by health insurance
- smoker: Smoking status
- region: Beneficiary's residential area
- charges: Individual medical costs billed by health insurance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/benefits-cost-optimization.git
cd benefits-cost-optimization
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Download the dataset:
- Visit https://www.kaggle.com/datasets/mirichoi0218/insurance
- Download the insurance.csv file
- Place it in the `data` directory

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar controls to:
- Adjust age range filters
- Simulate deductible changes
- View different time periods

## Project Structure
```
benefits-cost-optimization/
├── app.py              # Main Streamlit dashboard application
├── data/
│   └── insurance.csv   # Dataset (download from Kaggle)
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Analysis Methodology

### Cost Forecasting
- Utilizes Facebook Prophet for time series forecasting
- Incorporates seasonal patterns and trends
- Provides confidence intervals for predictions

### ROI Calculation
ROI is calculated using the formula:
```
ROI = (Cost Savings - Program Costs) / Program Costs * 100
```

### Cost Drivers Analysis
- Age-based cost correlation
- Impact of lifestyle factors (smoking status)
- Regional cost variations
- Family size impact

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
