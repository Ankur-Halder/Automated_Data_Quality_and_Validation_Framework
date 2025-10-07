import pandas as pd
import logging

def check_duplicates(df):
    duplicate_count = df.duplicated().sum()
    duplicate_percent = (duplicate_count / len(df)) * 100
    
    if duplicate_count > 0:
        logging.info("Duplicate Rows: %d", duplicate_count)
        logging.info("Duplicate %%: %.2f%%", duplicate_percent)
    else:
        logging.info("No duplicate rows found.")
    
    