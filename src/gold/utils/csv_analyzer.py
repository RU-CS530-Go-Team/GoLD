'''
Created on Dec 7, 2014

@author: JBlackmore
'''

import csv

def check_filter(row, key, val, op):
    if op=='=' or op=='==':
        filtered = row[key]==val
    elif op=='<' or op=='<=':
        filtered = float(row[key])<float(val)
        if op=='<=' and not filtered:
            filtered = float(row[key])==float(val)
    elif op=='>' or op=='>=':
        filtered = float(row[key])>float(val)
        if op=='>=' and not filtered:
            filtered = row[key]==val
    return filtered
'''
Expecting dict of {key, (value, op)}
or {key, (value,)} to use equality by default.
Valid ops are '==', '<', '<=', '>=', '>'
'''
def check_criteria(criteria, record):
    for key in criteria.keys():
        valOp = criteria[key]
        if len(valOp)<2:
            op = '=='
        else:
            op = valOp[1]
        val = valOp[0]
        satisfied = check_filter(record, key, val, op)
        if not satisfied:
            return False
    return True
        
def build_contingency_table(termcountfile, description=[], filter_dict=dict(), class1_dict=dict(), class2_dict=dict()):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        for line in description:
            print line
        #print('Black-to-live: ')
        #print('Terminal vs White groups increasing')
        for row in rdr: 
            filtered = not check_criteria(filter_dict, row)
            if not filtered:
                c1test = check_criteria(class1_dict, row)
                c2test = check_criteria(class2_dict, row)
                if 'COUNT' in row:
                    incr = int(row['COUNT'])
                else:
                    incr = 1
                if c1test and c2test:
                    N11+=incr
                elif c1test:
                    N10+=incr
                elif c2test:
                    N01+=incr
                else:
                    N00+=incr
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))
        return [[N00, N01],[N10, N11]]

