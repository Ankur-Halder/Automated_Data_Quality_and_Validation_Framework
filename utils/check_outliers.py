import pandas as pd
import numpy as np
import logging

def check_outliers(df, z_thresh=3):
    numeric_df = df.select_dtypes(include=np.number)
    
    z_scores = (numeric_df - numeric_df.mean()) / numeric_df.std()
    outlier_mask = (np.abs(z_scores) > z_thresh).any(axis=1)
    
    outlier_count = outlier_mask.sum()
    outlier_percent = (outlier_count / len(df)) * 100
    
    if outlier_count > 0:
        logging.info("Outlier Rows: %d", outlier_count)
        logging.info("Outlier %%: %.2f%%", outlier_percent)
    else:
        logging.info("No outliers found.")
    
    