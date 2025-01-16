# House Price Predictor 🏡 🤑

## Requirements
Ensure you have Python installed, then install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage
Generate a `*.txt` file, which contains name of the streets that you wish to compare and use for price calculation. 

Example: 
```
Ingolfs Allé
Breidablik Allé
Heklas Allé
Geysers Allé
Gimles Allé
Thingvalla Allé
Højdevangs Allé
Ulrich Birchs Allé
Dronning Elisabeths Allé
Christian II's Allé
```

Now run `scrape_latest_sales_prices` with the `*.txt` file, a postal code and optionally a property type (house, terrace_house, villa_apartment, and summerhouse). 

```shell
> python -m scrape_latest_sales_prices examples/[FILENAME].txt [POSTAL CODE] *[PROPERTY_TYPE]*
```

For example: 
```shell
> python -m scrape_latest_sales_prices examples/eberts_villaby.txt 2300 --property-type 'villa_apartment'
```

This will generate a `*.csv`-file with the results of the scraping. You can now use that csv-file to calculate a suggested price based on the house's area: 

```shell
> python -m predict_sales_price eberts_villaby.csv 180
```

### Narrow search
It is possible to alter certain criterias in `predict_sales_price`, as it takes the following parameters: 

```
    streets_csv (str): 
        Path to the CSV file containing sales data for various properties.
    house_area (int): 
        Size of the house (in square meters) for which the price is to be estimated.
    min_sales_year (int, optional): 
        The minimum year of property sales to include in the analysis. Defaults to `datetime.MINYEAR`.
    max_sales_year (int, optional): 
        The maximum year of property sales to include in the analysis. Defaults to the current year.
    min_area (int, optional): 
        The minimum size (in square meters) of properties to consider in the analysis. Defaults to 0.
    max_area (int, optional): 
        The maximum size (in square meters) of properties to consider in the analysis. Defaults to 9999.
    min_samples (int, optional): 
        The minimum number of sales samples required for the analysis. Defaults to 0.
```

For example: 
```shell
> python -m predict_sales_price eberts_villaby.csv 180 --min-sales-year=2010 --max-sales-year=2023 --min-area=100 --max-area=150 --min-samples=10
```

## File Descriptions
- **`scrape_latest_sales_prices.py`**: Main script for scraping sales data and estimating house prices.
- **`predict_sales_price.py`**: Main script for predicting price of house given area size.
- **`utils.py`**: Contains utility functions for processing and analyzing data. Useful for using functions in Python repl. 
- **`test_address_regex.py`**: Unit tests for validating address-related functions.
- **`requirements.txt`**: Lists all the dependencies required to run the project.
