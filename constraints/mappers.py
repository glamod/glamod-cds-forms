import sys
sys.path.append('../../cdm-lens/cdm_interface')

from wfs_mappings import wfs_mappings


name_mappers = {
    'report_type': 'frequency',
    'data_policy_licence': 'intended_use',
    'quality_flag': 'data_quality',
    'variable': 'variable' 
}


special_cases = {
    'data_quality': (['quality_controlled'], ['all_data', 'quality_controlled'])
}


def rev_mapper(key):
    return dict([(v, k) for k, v in wfs_mappings[key]['fields'].items()])


def ftime(seq):
    "Format time list into strings of double digits"
    return [f'{tm:02d}' for tm in seq]


def add_time_inputs(d):
    """
    This function extends the input dictionary to add more time components:

    Depending on the frequency setting, add appropriate: "day" and "hour" values
    Adjusts dict in place, returns None

    Following this issue: https://github.com/glamod/glamod-ingest/issues/54
    - removed "hour" component - no longer added to the dictionary

    """
    one_day = [1]
    one_hour = [0]

    all_days = range(1, 32)
    all_hours = range(0, 24)
 
    f = d['frequency'][0]

    if f == 'monthly':
        d['day'] = ftime(one_day)
#        d['hour'] = ftime(one_hour)

    elif f == 'daily':
        d['day'] = ftime(all_days)
#        d['hour'] = ftime(one_hour)

    elif f == 'sub_daily':
        d['day'] = ftime(all_days)
#        d['hour'] = ftime(all_hours)


def map_dict(din):
    dout = {}

    for key, value in din.items():
        nkey = name_mappers.get(key, key)

        if key in name_mappers:
            field_mapper = rev_mapper(nkey) 
            value = [field_mapper[_] for _ in value]

        dout[nkey] = value[:]

    print('[INFO] Applying special cases of superset mappings')
    for key, value in dout.items():
        for skey in special_cases:

            in_value, out_value = special_cases[skey]

            if key == skey and value == in_value:
                dout[key] = out_value

    return dout


def map_constraints(cin):
    cout = []

    for din in cin:
        dout = map_dict(din) 
        add_time_inputs(dout)
        cout.append(dout)

    return cout



def test_mappers():
    cin = [{'quality_flag': ['0'], 'report_type': ['3'], 'frequency': ['daily'],
            'data_policy_licence': ['0'], 'variable': ['44']}]
    cout = map_constraints(cin)

    print(cout)
    assert(cout == [{'data_quality': ['all_data', 'quality_controlled'],
                     'frequency': ['daily'],
                     'variable': ['accumulated_precipitation'],
                     'day': ftime(range(1, 32)), 
                     'hour': ftime([0]), 
                     'intended_use': ['open']}])


if __name__ == '__main__':

    test_mappers()
