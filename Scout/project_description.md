# Scout
## Introduction
Scout is a Machine Learning Algorithm built on (then) State-of-the-Art Temporal Fusion Transformer Architecture to predict Rent/SqFt Pricing of Multi-Family properties across the United States.

## Creators
**Tiago Da Costa** [2019-2021]

**Jason Belisario** [2019-2021]

**Emily Costa** [2019-2020]

## Relevant File Descriptions
### ../
- [Scout_1_6_1_GPU](Scout/Scout_1_6_1_GPU.ipynb): The latest version of the Temporal Fusion Transformer model implemented to predict Rent/SqFt Pricing.
- [Scout_TFT_pytorch](Scout/Scout_TFT_pytorch.ipynb): The initial version of the Temporal Fusion Transformer model implemented to predcit Rent/SqFt pricing. Based off the PyTorch Forecasting library's example of implementation.
- [Scout_Data_Clean](Scout/Scout_Data_Clean.ipynb): Program to join and clean our dataset with further data sources with differing levels of granularity such as: Macroeconomic data, Residential Housing Market Performance, and more. 
- [15 Miami.csv](<Scout/15 Miami.csv>): A dictionary of submarket names to submarket IDs.
### ../functions/
- [text](Scout/functions/market_dictionary.py): Create a SubmarketID Dictionary from a given PropertyData.csv file for an individual market.
- [text](Scout/functions/PropertyIdFixes.py): Program containing functions to fix property ID in Data CSVs by either:
    1) Fixing the existing property IDs by concatenating the market and submarket
        codes to them.
    2) Adding them to a CSV if not present by matching properties in said CSV
     with their counterparts in another CSV which contains property IDs using
     another indicator of similarity such as address or property name.
### ../functions/Financial Modeling/
- [FeatureSupportFunctions.py](<Scout/functions/Financial Modeling/FeatureSupportFunctions.py>): Functions used to manipulate the dataset and to extract addtional features from loan data for use in creating financial models for the property markets.
- [FixLoansSales.py](<Scout/functions/Financial Modeling/FixLoansSales.py>): A program to fix issues in the loans and sales related columns in our datasets.
- [fixTimeIndices.py](<Scout/functions/Financial Modeling/fixTimeIndices.py>): A program to fix date formats from mm/dd/yyyy to yyyy-mm-dd in our datasets.
- [genModels.py](<Scout/functions/Financial Modeling/genModels.py>): The Main file for Financial Modeling. Used to run the functions to generate the financial models for each of the markets and submarkets. Included single threaded and multi-threaded implementations.
- [model_formulas.py](<Scout/functions/Financial Modeling/model_formulas.py>): A support program which defines many formulas commonly used in real estate financial modeling.
- [modelFeatGeneration.py](<Scout/functions/Financial Modeling/modelFeatGeneration.py>): A program which generates the new features created through using the above formulas with our dataset to create financial models for properties in each market and submarket.
- [done.txt](<Scout/functions/Financial Modeling/done.txt>): A list of all markets and submarkets for whom financial models have been made.
### ../Emily Costa/
Data wrangling fuctions written by our early contributer Emily Costa. Used to clean and interpolate the original dataset.

## Changes made for this display
- Removed API keys
- Removed Project ID
- Removed GCS Directories
- Removed Local Directories and Paths
- Removed Datasets
- Clarified Authorship and Source material

## References

Lim, B., Arık, S. Ö., Loeff, N., & Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. International Journal of Forecasting, 37(4), 1748-1764. https://doi.org/10.1016/j.ijforecast.2021.03.012

https://pytorch-forecasting.readthedocs.io/en/stable/index.html