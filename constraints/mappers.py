import sys
sys.path.append('../../cdm-lens/cdm_interface')

import copy

from wfs_mappings import wfs_mappings


name_mappers = {
    'report_type': 'frequency',
    'data_policy_licence': 'intended_use',
    'quality_flag': 'data_quality',
    'variable': 'variable' 
}

#special_cases = { 'data_quality': (['quality_controlled'], ['all_data', 'quality_controlled']) }

DAY_MONTHS = {
    31: ['01', '03', '05', '07', '08', '10', '12'],
    30: ['04', '06', '09', '11'],
    28: ['02']
}


def rev_mapper(key):
    return dict([(v, k) for k, v in wfs_mappings[key]['fields'].items()])


def ftime(seq):
    "Format time list into strings of double digits"
    return [f'{tm:02d}' for tm in seq]


def gather_months_by_length(months, n_days):
    print(months, n_days, set(DAY_MONTHS[n_days]) & set(months))
    return list(set(DAY_MONTHS[n_days]) & set(months))


def replicate_record_for_months(din, months, n_days):
    """Returns a replice of dictionary `din` where the 'month' is `months` and 'day' is a list
    of formatted days from ["01", ... "{n_days}"]
    """
    dout = copy.deepcopy(din)

    dout['month'] = months
    dout['day'] = ftime(range(1, n_days + 1))

    return dout


def expand_over_months(din):
    """Looks up months and then expands one dict into a list of dicts by grouping
    months of similar length per dict.
    
    Returns: list of dictionaries.
    """
    months = din['month']
    new_records = []

    for n_days in sorted(DAY_MONTHS.keys()):
        picked_months = gather_months_by_length(months, n_days)
        if not picked_months: continue

        print(picked_months)
        new_record = replicate_record_for_months(din, picked_months, n_days)
        new_records.append(new_record)

    return new_records


def NOT_USED_add_time_inputs(d):
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
    """Apply mappers to input dictionary, into output dictionary.

    Args:
        din ([dict]): input constraints

    Returns:
        [dict]: output constraints
    """
    dout = {}

    for key, value in din.items():
        nkey = name_mappers.get(key, key)

        if key in name_mappers:
            field_mapper = rev_mapper(nkey) 
            value = [field_mapper[_] for _ in value]

        dout[nkey] = value[:]

#    print('[INFO] Applying special cases of superset mappings')
#    for key, value in dout.items():
#        for skey in special_cases:
#            in_value, out_value = special_cases[skey]
#            if key == skey and value == in_value:
#                dout[key] = out_value

    return dout


def map_constraints(cin):
    """Takes in a list of dictionaries of constraints.
    For each dictionary:
     - constraints are mapped

    A new list of dictionaries is returned.
    """
    cout = []

    for din in cin:
        dout = map_dict(din) 
#        add_time_inputs(dout)
#        expanded_douts = expand_over_months(dout)
#        cout.extend(expanded_douts)
        cout.append(dout)

    return cout



def test_mappers():
    cin = [{'quality_flag': ['0'], 'report_type': ['3'], 'frequency': ['daily'],
            'data_policy_licence': ['0'], 'variable': ['44'], 'month': ['01', '02', '03', '04']}]
    cout = map_constraints(cin)

    expected ={'data_quality': ['all_data', 'quality_controlled'],
                     'frequency': ['daily'],
                     'variable': ['accumulated_precipitation'],
 #                    'day': ftime(range(1, 32)), 
 #                    'hour': ftime([0]), 
                     'intended_use': ['open']}

    exp1 = copy.deepcopy(expected)
    exp1.update({'month': ['02'], 'day': ftime(range(1, 29))})
    print(cout[0])
    print(exp1)
    assert(cout[0] == exp1)

    exp2 = copy.deepcopy(expected)
    exp2.update({'month': ['04'], 'day': ftime(range(1, 31))})
    print(cout[1])
    print(exp2)
    assert(cout[1] == exp2)

    exp3 = copy.deepcopy(expected)
    exp3.update({'month': ['01', '03'], 'day': ftime(range(1, 32))})
    print(cout[2])
    print(exp3)
    assert(cout[2] == exp3)

    print("[SUCCESS] All passed!")


if __name__ == '__main__':

    test_mappers()
