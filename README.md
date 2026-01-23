
---
# 👗 Women's E-Commerce Review Analyzer

A comprehensive Python package designed to analyze, visualize, and extract insights from e-commerce clothing reviews. This project combines traditional statistical analysis with Natural Language Processing (NLP) to understand consumer behavior patterns.

It features an **interactive Dashboard** built with Streamlit.

![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)

---

## 📋 Project Description

The goal of this project is to analyze a dataset of women's clothing reviews to identify key drivers of customer satisfaction. The tool allows for raw data cleaning, demographic visualization, and sentiment analysis (using VADER) to correlate written opinions with numerical ratings.

### 🌟 Key Features

* **Data Ingestion & Cleaning (`DataLoader`)**:
    * Automated cleaning of column names and handling of missing values.
    * **Feature Engineering**: Creation of 'Age Groups' and merging of Review Titles with Body Text.
* **Statistical Visualization (`DataVisualizer`)**:
    * Dynamic generation of histograms and bar charts.
    * **Advanced Heatmaps**: Analysis of categorical variables (e.g., Department vs. Recommendation Rate).
    * Smart detection of skewed data to automatically apply logarithmic scales.
* **Text & NLP Analysis (`TextAnalyzer`)**:
    * Text Preprocessing (HTML tag removal, URL stripping, and normalization).
    * **VADER Sentiment Analysis**: Automatic classification into Positive, Neutral, and Negative sentiments.
    * **Semantic Mining**: Visualization of WordClouds and Top N-Grams (Bigrams/Trigrams) for specific sentiments.
* **Interactive Web Interface**: A complete Dashboard powered by Streamlit to explore data without writing code.

---

## 🛠️ Project Structure

```text
ecomm_review_analyzer/
├── ecomm_review_analyzer/          # Main Source Code Package
│   ├── __init__.py                 # Package initialization
│   ├── data_loader.py              # Logic for loading, cleaning, and transforming data
│   ├── data_visualizer.py          # Logic for statistical plotting (Matplotlib/Seaborn)
│   ├── text_analyzer.py            # Logic for NLP, VADER sentiment analysis, and N-grams
│   ├── main.py                     # main
│   └── errors.py                   # Custom exception definitions for error handling
│
├── data/                           # Data Directory
│   └── Womens Clothing...csv       # Raw dataset (usually excluded from version control)
│
├── docs/                           # Extended Documentation
│   ├── en/INSTRUCTIONS.md          # Detailed setup instructions in English
│   └── es/INSTRUCTIONS.md          # Detailed setup instructions in Spanish
│
├── app.py                          # Streamlit Application (Web Dashboard entry point)
├── plot.ipynb                      # Jupyter Notebook (Used for prototyping/EDA)
│
├── requirements.txt                # Production dependencies (for end-users)
├── requirements_dev.txt            # Development dependencies (for contributors/testing)
├── README.MD                       # Documentation
│
├── setup.py                        # Installation script for the package
├── setup.cfg                       # Static configuration for package metadata
├── pyproject.toml                  # Modern build system configuration
├── Makefile.txt                    # Automation shortcuts (install, test, clean)
│
├── CHANGELOG.md                    # History of changes and versions
├── VERSION.txt                     # Single source of truth for the project version
└── LICENSE.txt                     # MIT License terms
```

### 🚀 Installation & Usage

1.  **Install the package (.whl):**
    ```bash
    pip install ecomm_review_analyzer-1.0.0-py3-none-any.whl
    ```
    
2.  **Running the Dashboard (Streamlit)** To launch the interactive Streamlit interface:
    ```bash
    streamlit run app.py
    ```
    To stop the dashboard, press `Ctrl + C` in the terminal.
    

### 💡 Usage Example

1. To use the library programmatically in a Python script or Jupyter Notebook:
    ```bash
    import ecomm_review_analyzer as era

    # 1. Load and process data
    loader = era.DataLoader()
    df = (loader.load_data("data/Womens Clothing E-Commerce Reviews.csv")
                .clean_data()
                .process_ecommerce_data()
                .df)
    ``` 
2. Visualizer:
    ```bash
    viz = era.DataVisualizer(df)
    viz.plot_histogram(column_name="Age") # Generate histogram for Age column 
    ```

3. Text Analyzer:
    ```bash
    text_viz = era.TextAnalyzer(df)
    text_viz.analyze_sentiment_vader() # in order to generate "Sentiment" column
    my_stopwords = text_viz.get_stopwords(extra_words=["dress", "petite", "made", "will"])
    text_viz.plot_wordcloud(sentiment="Positive", stopwords=my_stopwords)
    ```


   