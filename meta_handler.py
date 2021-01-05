import pandas as pd


class MetaHandler:
    def __init__(self):
        self.dummy_user = None

    @staticmethod
    def format_user_form_data(_form):
        # get languages from form input
        _user_languages = _form.getlist('languages')

        # create user dict
        _user = {
            'age': int(_form.get('age')),
            'country': int(_form.get('country')),
            'gender': _form.get('gender'),
        }

        # assign languages to user
        for l in _user_languages:
            _user[l] = 1

        return _user

    def create_dummy_user(self, _form):
        if not _form:
            # default filter settings..
            _user = {
                'age': 23,
                'country': 4,
                'gender': 'm',
            }
        else:
            _user = self.format_user_form_data(_form)

        # create df and fill NaN values with 0
        _user = pd.DataFrame(_user, index=['-1'])
        _user = _user.fillna(0)

        # reindex user
        _user = _user.reindex(sorted(_user.columns), axis='columns').fillna(0).tail(1)

        self.dummy_user = _user

        return _user

    def get_dummy_user(self):
        return self.dummy_user

    @staticmethod
    def get_programming_languages():
        return pd.read_csv('meta/languages.csv', usecols=['name'])['name'].tolist()

    @staticmethod
    def get_countries():
        _results = pd.read_csv('meta/countries.csv', usecols=['name'])

        def format_row(_val):
            if isinstance(_val, str):
                _val = _val.lower().replace(' ', '_').replace('-', '_')
            return _val

        _results = _results.applymap(format_row)

        return _results['name'].tolist()

