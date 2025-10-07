import pandas as pd
import logging

def check_missing_values(df):
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100
    missing = pd.DataFrame({
        'Missing Count': missing_count,
        'Missing %': missing_percent
    })
    
    missing_filtered = missing[missing['Missing Count'] > 0]
    total_missing_percentage = df.isnull().sum().sum()/df.count().sum()*100
    total_loss ={ 'Missing Count': df.isnull().sum().sum(),
        'Missing %':( total_missing_percentage)}
    total_df = pd.DataFrame(total_loss,index=["total_loss"])
    missing_filtered = pd.concat([missing_filtered,total_df])
    if not missing_filtered.empty:
        logging.info("\n%s", missing_filtered.to_string())
        if total_missing_percentage>5.0:
            logging.warning("Missing Percentage is More Than The Required Thereshold, Initating  Data Pre-Processing")
            return True
    else:
        logging.info("No missing values found.")
        return False
    
