from datetime import (
    datetime
)

from dateutil import relativedelta

def add_datestamp():
    """Getting a time stamp link

    Returns:
        datetime_string : string of date string
    """
    datetime_string = datetime.today().strftime('%d_%m_%Y_%H_%M')

    return datetime_string

def monthly_interval_list(start_date, end_date):
    
    #Differnce in months
    delta = relativedelta.relativedelta(end_date, start_date)

    res_months = delta.months + (delta.years * 12)

    interval_array = [start_date + relativedelta.relativedelta(months=each_month) for each_month in range(res_months+1)]

    return interval_array


def rolling_6_month_sum(
        dataframe,
        date_column,
        date_interval,
        column_group
):
    """Calculates the rolling 6 month sum for a given dataframe.

    Args:
        dataframe (pd.DataFrame): The input dataframe.
        date_column (str): The name of the date column in the dataframe.
        date_interval (list) List of date intervals to consider for rolling sum.
        column_group (list) List of the col names to group by

    Returns:
        pd.DataFrame: Dataframe with rolling 6 month sum.
    """

    #First need to get the unique combination from column group
    unqiue_combination = dataframe.drop_duplicates(subset=[column_group])

    for each thet