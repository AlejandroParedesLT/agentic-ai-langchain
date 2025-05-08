import pandas as pd
from src.servers.dataAnalysis.model import DataAnalysisOutput

def statistics(csv):
    """
    Creates a JSON-style dictionary with essential statistics for numerical columns.

    Args:
        csv (str): Path to a CSV file with structured information.

    Returns:
        dict: Dictionary with keys {count, mean, std, median, kurtosis, min, max} for each numerical column.
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    df = pd.read_csv(csv)

    # Select only numerical columns
    numeric_df = df.select_dtypes(include='number')

    # Compute required statistics
    stats = {
        "count": numeric_df.count().to_dict(),
        "mean": numeric_df.mean().to_dict(),
        "std": numeric_df.std().to_dict(),
        "median": numeric_df.median().to_dict(),
        "kurtosis": numeric_df.kurtosis().to_dict(),
        "min": numeric_df.min().to_dict(),
        "max": numeric_df.max().to_dict(),
    }

    return DataAnalysisOutput(output=stats)
