import datetime
from main_dec import main
from utils import read_prices, predict_sales_price

@main
def _(
    streets_csv: str,
    house_area: int,
    min_sales_year: int = datetime.MINYEAR,
    max_sales_year: int = datetime.datetime.today().year,
    min_area: int = 0,
    max_area: int = 9999,
    min_samples: int = 0,
) -> None:
    prices = read_prices(streets_csv)
    price = predict_sales_price(
        prices=prices,
        house_area=house_area,
        min_sales_year=min_sales_year,
        max_sales_year=max_sales_year,
        min_area=min_area,
        max_area=max_area,
        min_samples=min_samples
    )
    price = '{:,.2f} kr.'.format(price)
    print(f"Suggested price for house of size {house_area} situated in {prices.zip_code[0]}: {price}")
          