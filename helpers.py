from currency_converter import CurrencyConverter


c = CurrencyConverter()


# prepare records for sending to FE
def format_records_for_fe(_records):
    # record field that just get copied 1:1
    default_meta_fields = ['age', 'gender', 'workweekhrs', 'overtime',
                           'employment', 'similarity', 'salary', 'user', 'country']
    _new_list = []

    for r in _records:
        # create new item
        _new_item = {'languages': []}

        # iterate through object keys (attrs)
        for x in list(r):
            if x in default_meta_fields:
                _new_item[x] = r[x]

            else:
                if r[x] != 0:
                    _new_item['languages'].append(x)

        _new_list.append(_new_item)

    return _new_list


# update gender with m/f/d
def update_gender_field(_val):
    if _val['gender'] == 'man':
        _gender = 'm'
    elif _val['gender'] == 'woman':
        _gender = 'w'
    elif _val['gender'] == 'non_binary,_genderqueer,_or_gender_non_conforming':
        _gender = 'd'
    else:
        _gender = 'n/a'

    _val['gender'] = _gender

    return _val


# cut a string after ':'
def cut_string(_val):
    return _val.split(':')[0]


# lowercase and replace spaces and '-' with underscores
def format_row(_val):
    if isinstance(_val, str):
        _val = _val.lower().replace(' ', '_').replace('-', '_')
    return _val


# convert salary based on currency & pay rate
def calc_real_salary(_val):
    # try to convert currency
    try:
        _val['convertedcomp'] = c.convert(_val['convertedcomp'], _val['currencysymbol'].upper(), 'EUR')
    except ValueError:
        return _val

    # multiple by 12 if pay is monthly
    if _val['compfreq'] == 'monthly':
        _val['convertedcomp'] = _val['convertedcomp'] * 12

    return _val


# For each programming language we want a dedicated column
def split_languages(_val):
    langs = _val['languageworkedwith'].split(';')

    for l in langs:
        _val[l] = 1

    return _val

