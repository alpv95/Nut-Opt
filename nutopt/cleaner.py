import pandas as pd

from nutopt.utils import *

def clean_data():
    '''
    This function cleans the data by removing the columns that are not needed.

    Input: None
    Output: Dataframe
    '''
    df = pd.read_csv('../data/nutrition.csv').drop(['Unnamed: 0', 'serving_size'], axis=1)
    # use the name as the index 
    df = df.drop('lucopene', axis=1)
    df = df.drop('fatty_acids_total_trans', axis=1)
    df = df.drop('tocopherol_alpha', axis=1)

    #Foods to be removed
    current_names = df['name']
    flags = ['babyfood', 'infant','dried','beverage','leavening','stevia','toddler']
    remove = [idx for idx in range(len(df)) if any([label in current_names.iloc[idx].lower() for label in flags])]
    df = df.drop(remove,axis=0)

    units = df.iloc[1].apply(get_unit).to_dict()
    units['calories'] = 'kcal'
    units['hydroxyproline'] = 'g'
    units['galactose'] = 'g'
    units['cholesterol'] = 'mg'

    cols_with_unit = df.columns.drop(['calories'])
    for col in df[cols_with_unit]:
        df[col] = df[col].apply(delete_unit)

    return df

def subselect_data(df: pd.DataFrame, foods: list):
    '''
    This function subselects the data by the list of foods that we want to look at.

    Input: Dataframe, list of foods
    Output: Dataframe
    '''
    assert len(foods) != 0, "Please enter a list of foods"

    mask = df['name'].str.contains(foods[0])
    for food in foods[1:]:
        mask |= df['name'].str.contains(food)
    df = df[mask]
    return df