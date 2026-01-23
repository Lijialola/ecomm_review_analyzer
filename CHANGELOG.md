# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## [1.0.0] - 2026-01-17
### Added
- **Initial Release**: Comprehensive `ecomm_review_analyzer` package for retail data analysis.
- **DataLoader**: Implemented automated cleaning, duplicate removal, and feature engineering for age groups and text merging.
- **DataVisualizer**: Core visualization module with automated canvas management (`_setup_canvas` and `_finalize_canvas`) to ensure DRY principles.
- **TextAnalyzer**: Advanced NLP module featuring VADER sentiment analysis, WordCloud generation, and N-gram frequency plotting.
- **Interactive Dashboard**: Integrated Streamlit application (`app.py`) for user-friendly data exploration and real-time analysis.

### Changed (Refactoring)
- Applied **Single Responsibility Principle (SRP)** across all modules to separate data calculation from visualization logic.
- Refactored plotting functions to support both standalone figures and existing Matplotlib axes.

## [0.2.0] - 2025-12-23
### Added
- **Core ETL Logic**: Developed the primary data processing pipeline in `DataLoader`.
- **Statistical Foundations**: Implemented the first set of visualization methods (Histograms and Bar Charts) in `DataVisualizer`.
- **NLP Integration**: Added `TextAnalyzer` class with initial support for VADER sentiment scoring and basic text cleaning.
- **Error Handling**: Introduced custom exceptions in `errors.py` to handle missing columns and empty datasets.
- **Categorical Analysis**: Added heatmap support for cross-tabulation of categorical variables.

### Fixed
- Improved text preprocessing to handle HTML tags and special characters in reviews.
- Resolved axis overlapping issues in multi-plot figures.
- Optimized memory usage during large WordCloud generation.

## [0.1.0] - 2025-12-05
### Added
- Project template and base directory structure.
- Initial configuration for `setup.py`, `setup.cfg`, and `requirements_dev.txt`.