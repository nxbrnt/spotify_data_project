#Not Pythonic. This is only so pandas import is included in groupby_lists.py
#Otherwise, pandas is not in the module's namespace.
import pandas as pd

def groupby_lists(df, col, col_name):
    """
    Groupby function for a column of lists.

    This gives a one to many grouping with one group per unique element in the 
    union of all of lists in a column. A row in the original dataframe will 
    appear in multiple groups, so the resulting number of rows will typically 
    be larger than the number of rows in the original dataframe. 
    
    Parameters
    ----------
    df : Pandas DataFrame
    col : str
        The column of lists to group by.
    col_name : str
        A name for the resulting grouped column. e.g. if the original column 
        of lists was named 'models', a natural value for col_name would be 
        'model'.

    Returns
    -------
    Pandas GroupBy object

    """

    cols = df.columns
    
    #Expand list elements out to separate columns. Number of columns determined
    #by longest list. All rows padded with NaN to have same number of columns. 
    #The resulting column labels have no meaning aside from indicating the 
    #position of each list element in the original list it came from
    #e.g. element 0, element 1, etc.
    df_exp = df[col].apply(pd.Series)
    
    #Join expanded lists with original dataframe
    df_exp = df_exp.join(df)
    
    #"Unpivot" expanded list columns. Effectively duplicates every row N times 
    #where N is the number of elements in the row's corresponding list.
    #id_vars is every column except for the expanded list columns.
    #col_name labels the resulting column of individual list elements.
    df_exp = df_exp.melt(id_vars=cols,value_name=col_name)
    
    #Drop the original column of lists, as well as superfluous 'variable' 
    #column from melt (which simply indicates the original position of the 
    #element in its corresponding list)
    df_exp = df_exp.drop([col,'variable'],axis=1)
    
    #Group by column of individual list elements.
    grouped = df_exp.groupby(col_name)
    
    return grouped