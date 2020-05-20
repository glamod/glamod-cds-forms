import sys
sys.path.append('/usr/local/cdm_lens/src/cdm_lens/cdm_interface')

from wfs_mappings import wfs_mappings

"""

{'target': 'quality_flag', 'fields': {'quality_controlled': '0', 'all_data': '1'}, 'labels': {'quality_controlled': 'Quality controlled', 'all_data': 'All data'}, 'values': ['quality_controlled', 'all_data'], 'indent': 3}


        d = {}
        d['domain'] = kwargs['domain']

        d['report_type'] = self._map_value('frequency', kwargs['frequency'],
                                wfs_mappings['frequency']['fields'])

        if 'bbox' in kwargs:
            bbox = [float(_) for _ in kwargs['bbox'].split(',')]
            d['linestring'] = self._bbox_to_linestring(*bbox)
            tmpl += "ST_Intersects({linestring}, location) AND "

        d['observed_variable'] = self._map_value('variable', kwargs['variable'],
                                     wfs_mappings['variable']['fields'],
                                     as_list=True)

        d['data_policy_licence'] = self._map_value('intended_use', kwargs['intended_use'],
                                     wfs_mappings['intended_use']['fields'])

        if kwargs.get('data_quality', None) == 'quality_controlled':
            # Only include quality flag if set to QC'd data only
            d['quality_flag'] = '0'
            tmpl += "quality_flag = {quality_flag} AND "


dict_keys(['frequency', 'variable', 'intended_use', 'data_quality', 'column_selection', 'year', 'month', 'day', 'hour', 'format'])

"""

name_mappers = {
    'report_type': 'frequency',
    'data_policy_licence': 'intended_use',
    'quality_flag': 'data_quality'
}


def rev_mapper(key):
    return dict([(v, k) for k, v in wfs_mappings[key]['fields'].items()])


def map_dict(din):
    dout = {}

    for key, value in din.items():
        nkey = name_mappers.get(key, key)

        if key in name_mappers:
            field_mapper = rev_mapper(nkey) 
            value = [field_mapper[_] for _ in value]

        dout[nkey] = value[:]

    return dout


def map_constraints(cin):
    cout = []

    for din in cin:
        dout = map_dict(din) 

        cout.append(dout)

    return cout



def test_1():
    cin = [{'quality_flag': ['0'], 'report_type': ['2']}]
    cout = map_constraints(cin)
    print(cout)
    assert(cout == [{'data_quality': ['quality_controlled'],
                     'frequency': ['monthly']}])

test_1()
