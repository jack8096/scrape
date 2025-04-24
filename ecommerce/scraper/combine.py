import pandas as pd
from .amazon import AmazonScraper
from .flipkart import FlipkartScraper
from .myntra import MyntraScraper


def combine_results(search_term: str) -> pd.DataFrame:
    # Initialize scrapers
    amazon_scraper = AmazonScraper(search_term)
    flipkart_scraper = FlipkartScraper(search_term)
    myntra_scraper = MyntraScraper(search_term)

    # Fetch results from each
    amazon_results = amazon_scraper.get_results()
    flipkart_results = flipkart_scraper.get_results()
    myntra_results = myntra_scraper.get_results()

    # Combine into a single DataFrame
    combined_df = pd.DataFrame(amazon_results + flipkart_results + myntra_results)

    # Convert rating to float for sorting
    if "rating" in combined_df.columns:
        combined_df["rating"] = pd.to_numeric(combined_df["rating"], errors="coerce")

    # Sort by rating (highest first)
    combined_df = combined_df.sort_values(
        by="rating", ascending=False, na_position="last"
    )

    return combined_df.reset_index(drop=True)


if __name__ == "__main__":
    df = combine_results("red dress")
    print(df.head())
