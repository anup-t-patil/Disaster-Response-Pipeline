# lets import necessary libraries
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """This function loads the data from two different files (message and categories)
    and merge them in pandas dataframe to return that dataframe
        
    """
    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)   
    df = messages.merge(categories, how='inner', on='id')
    
    return df


   


def clean_data(df):
    
    
    """
    This function is used to clean the dataframe 
    
    Arguments:
        df: Pandas DataFrame having categoris and message data
    Outputs:
        df: Pandas DataFrame with preprocessed data
    """
    
    categories = df['categories'].str.split(";",expand=True)
    row = categories.iloc[0,:]
    category_colnames = row.apply(lambda x: x[:-2])
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].apply(lambda x: x[-1])
        # convert column from string to numeric
        categories[column] = categories[column].apply(lambda x: pd.to_numeric(x))
    
    categories['related']=categories['related'].replace(2,0)
    
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    df = df.drop_duplicates()
    
    return df
    

def save_data(df, database_filename):
    
    """
    This function is used to save the preprocessed data to database file
    
    Arguments:
        df-preprocessed dataFrame
        database_filename database file (.db) destination path
    """
    engine = create_engine('sqlite:///{}'.format(database_filename))
    table_name = database_filename.replace(".db","") + "_table"
    df.to_sql('df', engine, index=False, if_exists='replace')


def main():
    
    """ 
    Main function to execute ETL pipeline
    
    """
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()