# UC Transfer Admission Stats Visualization Web App
![Demo](https://github.com/ayumu0622/UC-Transfer-Analyzer/assets/67722808/e610b253-c936-40ed-9eeb-ce1b332937d1)

## Overview

Welcome to the UC Transfer Admission Stats Visualization Web App repository! This project focuses on visualizing UC Transfer statistics, specifically admit rates and enrollment numbers, categorized by majors. The web app can be accessed [here](https://uc-transfer-admission-stats-visualization-tool.streamlit.app).

## Data Source

The dataset powering these visualizations was sourced from the [University of California Information Center](https://www.universityofcalifornia.edu/about-us/information-center/transfers-major). It spans a decade and encompasses admission statistics for each major.

## Motivation

The motivation behind this web app stems from my own experience navigating through college admission stats on the University of California website. Recognizing the need for a more user-friendly approach, I developed this tool to empower community college students in choosing majors when applying to UC schools.

## Technical Details

- **Data Retrieval**: Utilizing MySQL skills, I wrote a parametrized query for BigQuery to retrieve data through API.
- **Preprocessing**: The data underwent preprocessing using Pandas to enhance its effectiveness in visualization.
- **Machine Learning**: Ridge regression models were built for each major using 10 years of statistics data (500-600 rows). This allows for predicting next year's admit rate from the current year's enrollment information, aiding potential applicants in choosing less competitive majors for UC Berkeley or UCLA.
- **Feature Engineering**: I implemented feature engineering and removed features with correlations to deal with multicollinearity.
- **Model Selection**: Ridge regression was chosen over normal multiple linear regression to avoid overfitting and provide more generalized predictions.

## Web App

Explore the web app [here](https://uc-transfer-admission-stats-visualization-tool.streamlit.app). It offers an intuitive interface for gaining insights into admission trends for different majors.

## Usage

To run the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/ayumu0622/UC-Transfer-Analyzer.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the web app: `streamlit run app.py`

## Conclusion

This project aims to simplify the college major selection process for transfer students, providing a valuable tool for making informed decisions. Contributions and feedback are highly welcome.

## License

This project is licensed under the MIT License.
