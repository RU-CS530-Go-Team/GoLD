'''
Created on Dec 7, 2014

@author: JBlackmore
'''
import sys
import csv
from gold.extraneous.csv_analyzer import build_contingency_table

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
        
def check_term_counts_for(termcountfile, description=[], filter_dict=dict(), class1_dict=dict(), class2_dict=dict()):
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
                if c1test and c2test:
                    N11+=int(row['COUNT'])
                elif c1test:
                    N10+=int(row['COUNT'])
                elif c2test:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))



def check_term_counts_9(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Correct vs White groups increasing and black not increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['SOL']=='1'
                binc = int(row['NW'])>0 and int(row['NB'])==0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))


def check_term_counts_8(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Correct vs White groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['SOL']=='1'
                binc = int(row['NW'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))


def check_term_counts_7(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Terminal vs White groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['TERM']=='1'
                binc = int(row['NW'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts_6(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Incorrect vs White groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['SOL']=='0'
                binc = int(row['NW'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts_5(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Incorrect+Terminal vs White groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['TERM']=='1' and row['SOL']=='0'
                binc = int(row['NW'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts_4(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Terminal vs Black groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['TERM']=='1'
                binc = int(row['NB'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts_3(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Solution vs Black groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['SOL']=='1'
                binc = int(row['NB'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts_2(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        N00=N01=N10=N11=0
        print('Black-to-live: ')
        print('Solution+Terminal vs Black groups increasing')
        for row in rdr: 
            if row['PT']=='1':
                solterm = row['SOL']=='1' and row['TERM']=='1'
                binc = int(row['NB'])>0
                if solterm and binc:
                    N11+=int(row['COUNT'])
                elif solterm:
                    N10+=int(row['COUNT'])
                elif binc:
                    N01+=int(row['COUNT'])
                else:
                    N00+=int(row['COUNT'])
        print('{} {}'.format(N00, N01))
        print('{} {}'.format(N10, N11))

def check_term_counts(termcountfile):
    with open (termcountfile, 'r') as termcountcsv:
        rdr = csv.DictReader(termcountcsv)
        termcountdicts = set([tuple(row.values()) for row in rdr])
        sol_term = [tuple(row) for row in termcountdicts if row['SOL']=='1' and row['TERM']=='1']
        black_incr = [tuple(row) for row in termcountdicts if int(row['NB'])>0]
        set1 = set(sol_term)
        set2 = set(black_incr)
        both = set1.intersection(set2)
        s1diffs2 = set1.difference(set2)
        s2diffs1 = set2.difference(set1)
        neither = termcountdicts.difference(set1).difference(set2)
        print('{} {}'.format(len(neither), len(s2diffs1)))
        print('{} {}'.format(len(s1diffs2), len(both)))

if __name__ == '__main__':
    termcountfile = sys.argv[1]
    check_term_counts_2(termcountfile)
    check_term_counts_4(termcountfile)
    check_term_counts_3(termcountfile)
    check_term_counts_5(termcountfile)
    check_term_counts_6(termcountfile)
    check_term_counts_7(termcountfile)
    check_term_counts_8(termcountfile)
    check_term_counts_9(termcountfile)
    desc = ['Black-to-live:','Solution+Terminal vs Black groups increasing']
    philter = {'PT': ('1','==')}
    class1 = {'SOL': ('1',), 'TERM':('1',)}
    class2 = {'NB': ('0','>')}
    build_contingency_table(termcountfile, desc, philter, class1, class2)
    desc[1] = 'Correct vs Black groups increasing'
    class1 = {'SOL': ('1',)}
    class2 = {'NB': ('0','>')}
    build_contingency_table(termcountfile, desc, philter, class1, class2)

    desc[1] = 'Solution vs Black groups decreasing'
    class1 = {'SOL': ('1',)}
    build_contingency_table(termcountfile, desc, philter, class1, class2)

    philter = {'PT': ('2',)}
    class1 = {'SOL': ('1',), 'TERM':('1',)}
    class2 = {'NB': ('0','>')}
    desc[0] = 'White-to-Kill'
    desc[1] = 'Solution+Terminal vs Black groups increasing'
    build_contingency_table(termcountfile, desc, philter, class1, class2)
    desc[1] = 'Solution vs Black groups increasing'
    class1 = {'SOL': ('1',)}
    build_contingency_table(termcountfile, desc, philter, class1, class2)
