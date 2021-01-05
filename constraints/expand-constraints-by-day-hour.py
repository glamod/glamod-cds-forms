#!/usr/bin/env python

"""
Reads in JSON contraints.

For each constraint:
 - maps to relevant day values if needed
  - maps to relevant hour values if needed
 - returns a list of constraints

Writes expanded constraints to JSON.

Needs to use sets:
 months = 1,3,5,7,8,10,12 --> all years --> days(1, 31) --> hours(0, 23)
 months = 2:
   years(1800 and 1900 AND all except divisible by 4) --> days(1,28) --> hours(0, 23)
   years(divisible by 4 excluding 1800 and 1900) --> days(1,29) --> hours(0, 23)
 months = 4,6,9,11 --> all years --> days(1, 30) --> hours(0, 23)
 
"""

import calendar as cal


d31_months = ['01', '03', '05', '07', '08', '10', '12']
d30_months = ['04', '06', '09', '11']

irregular_leap_years = [1800, 1900]


def get_feb_years_by_length(length, years):
    years = [int(_) for _ in years]

    if length == 28:
        res = set([_ for _ in years if _ % 4 != 0])
        for yr in irregular_leap_years:
            if yr in years:
                res.add(yr)

    elif length == 29:
        res = [_ for _ in years if _ % 4 == 0 and _ not in irregular_leap_years]

    return sorted([str(_) for _ in res])


assert(['1896'] == get_feb_years_by_length(29, ['1896', '1897', '1898', '1899', '1900']))
assert(['1900', '1901'] == get_feb_years_by_length(28, ['1900', '1901']))
