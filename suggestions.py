import pandas as pd
from helpers import format_records_for_fe


# display settings
pd.options.display.max_columns = 50
pd.options.display.float_format = '{:,.0f}'.format

# exceptions won't be counted during creating similarities, just for representation
exception_keys = ['workweekhrs', 'newovertime', 'gender', 'employment', 'user']

# only consider people with a age gap of max. {max_age_difference}yrs
max_age_difference = 7


class Suggestions:
    def __init__(self, meta_handler):
        self.meta_handler = meta_handler

    # calculate similarity between results & fake user
    # each skill/attr (except exception_keys) the user has gets compared to all aggregated users
    # if values match, score is increased by 1
    # if age or country don't match we take a portion of the points away because these are higher weighted attrs
    def sim_calc(self, _val):
        _user = self.meta_handler.get_dummy_user()
        _score = 0

        for key in _val.index:
            if key in exception_keys or key not in _user:
                continue

            _userval = _user[key]

            if int(_userval == 1) & int(_val[key] == 1):
                _score += 1
            else:
                if key == 'age' or key == 'country':
                    # age / country makes a larger difference
                    _diff = (abs(int(_val[key]) - int(_userval)) / 10) if key == 'age' else 3
                    _score -= _diff / 2

        _val['similarity'] = round(_score, 3)

        return _val

    # get similar users depending on the passed form-user-data
    def get_suggestions(self, _results, _form, _suggestions=30):
        _user = self.meta_handler.create_dummy_user(_form)

        print('calculating similarities for:')
        print(_user)

        # pre filter records to shrink computing time
        _results = _results.loc[
            (_results['gender'] == _user['gender'][0]) &
            (_results['age'] < (_user['age'][0] + max_age_difference)) &
            (_results['age'] > (_user['age'][0] - max_age_difference))]

        if _results.empty:
            return -1

        similarities = _results.apply(self.sim_calc, axis='columns')
        similarities = similarities.loc[similarities['similarity'] > 0]
        similarities = similarities.sort_values('similarity', ascending=False).head(_suggestions)

        print('done calculating')

        return format_records_for_fe(similarities.to_dict('records'))

    @staticmethod
    # get top 15 most earning users
    def get_top_users(_results):
        return format_records_for_fe(_results.sort_values('salary', ascending=False).head(15).to_dict('records'))

