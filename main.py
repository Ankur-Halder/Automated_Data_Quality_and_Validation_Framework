import pandas as pd
import numpy as np
import logging
import os
import sys
from datetime import datetime

logging.basicConfig(
    filename="data_quality.log",        
    level=logging.INFO,                 
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S"          
)

from utils import check_missing as missing
from utils import check_duplicate as duplicate
from utils import check_outliers,prep_data


if __name__ == "__main__":
    df = pd.read_csv("tested.csv")
    
    flag = missing.check_missing_values(df) # flag = missing_percentage >5%
    if flag:
        df = prep_data(df)

    duplicate.check_duplicates(df)

    check_outliers(df)

    print("Pipeline Sucessfull")
