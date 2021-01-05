import pandas as pd
import os.path
from helpers import (
    update_gender_field,
    cut_string,
    format_row,
    calc_real_salary,
    split_languages,
)


# aggregate original csv and create a new one
def aggregate_csv_data(meta_handler, overwrite=False):
    if os.path.exists('skill_salary.csv') and not overwrite:
        return

    # define columns & read csv
    result_names = ['Respondent', 'ConvertedComp', 'CompFreq', 'CurrencySymbol',
                    'Country', 'Age', 'Employment', 'LanguageWorkedWith',
                    'NEWOvertime', 'WorkWeekHrs', 'Gender']

    _results = pd.read_csv('survey_results_public.csv', usecols=result_names)

    # drop entries with NaN values
    _results.dropna(inplace=True)

    # lowercase and replace spaces and '-' with underscores
    _results = _results.applymap(format_row)

    # rename columns (same as above)
    _results.columns = _results.columns.str.replace(' ', '_')
    _results.columns = [x.lower() for x in _results.columns]

    # Now we calculate the real salary of each user (because we have monthly/yearly)
    _results = _results.apply(calc_real_salary, axis='columns')
    _results['convertedcomp'] = _results['convertedcomp'].astype(int)

    _results = _results.apply(update_gender_field, axis='columns')

    # drop the compfreq column -> not relevant anymore, also drop currencysymbol
    _results = _results.drop(['compfreq'], axis='columns')
    _results = _results.drop(['currencysymbol'], axis='columns')

    # For each programming language we want a dedicated column
    _results = _results.apply(split_languages, axis='columns')

    # also drop the languageworkedwith column -> we now have dedicated fields/language
    _results = _results.drop(['languageworkedwith'], axis='columns')

    # now we fill all NaN's with 0s
    _results = _results.fillna(0)

    _results['newovertime'] = _results['newovertime'].apply(cut_string)

    _countries = meta_handler.get_countries()

    def update_country_col(_val):
        _country = _countries.index(_val['country']) if _val['country'] in _countries else 0
        _val['country'] = _country
        return _val

    _results = _results.apply(update_country_col, axis='columns')

    # now we rename some cols
    _results = _results.rename(
        columns={'respondent': 'user',
                 'convertedcomp': 'salary',
                 'bash/shell/powershell': 'cmd',
                 'newovertime': 'overtime',
                 'c++': 'cpp',
                 'c#': 'csharp',
                 'html/css': 'html'})

    # reindex results
    _results = _results.reindex(sorted(_results.columns), axis='columns')

    # save result csv
    _results.to_csv('skill_salary.csv', index=False)


# load and return the saved csv
def load_csv():
    return pd.read_csv('skill_salary.csv')
