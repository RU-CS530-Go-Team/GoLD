'''
Created on Dec 4, 2014

@author: JBlackmore
'''
from numpy import ndarray, float64
from types import ListType, IntType, FloatType, StringType
import csv
from gold.features import *
'''
FEATURE_SERVICES = ['ColorFeature', 'StoneCountFeature', 'DiffLiberties', 'DistanceFromCenterFeature', 
                    'DistanceFromCenterFeature', 'numberLiveGroups', 'HuMomentsFeature',
                    'LocalShapesFeature', 'SparseDictionaryFeature']
'''
class FeatureExtractor():

    def __init__(self):
        pass

    def init_feature_services(self, start, move, movePosition, isblack):
        feature_services = dict()
        globals_hash = globals()
        services = globals()['FEATURE_SERVICES']
        #services = [s for s in FEATURE_SERVICES if s!='PatchExtractor']
        for service in services:
            feature_services[service] = globals_hash[service](start, move, movePosition, isblack)
            if service=='PatchExtractor':
                feature_services[service].setPatchSize(4)
        return feature_services

    def sort_headers(self, headers):
        sorted_headers = []
        f2x = ['ColorFeature'] + [h for h in headers if h[0]=='_']
        #globals_hash = globals()
        services = globals()['FEATURE_SERVICES']
        for fs in services: 
            if not fs in f2x:
                if fs in headers:
                    sorted_headers.append(fs)
                else:
                    i=1
                while ('{}_{}'.format(fs,i)) in headers:
                    sorted_headers.append('{}_{}'.format(fs,i))
                    i = i + 1
        return sorted_headers
          
    def extract_features(self, start, move, movePosition, isblack):
        feature_services = self.init_feature_services(start, move, movePosition, isblack)
        features = dict()
        for fk in feature_services.keys():
            fe = feature_services[fk]
            featureValue = fe.calculate_feature()
            fvtype = type(featureValue)
            if fvtype == ListType:
                for i,v in enumerate(featureValue):
                    features['{}_{}'.format(fe.name(),i+1)] = v
            elif fvtype in [IntType, FloatType, StringType, float64]:
                features[fe.name()] = featureValue
            elif fvtype == ndarray:
                for i,v in enumerate(featureValue):
                    # not sure this is how the feature should be output...
                    if( type(v)==ndarray ):
                        for j,vv in enumerate(v):
                            features['{}_{}_{}'.format(fe.name(),i+1,j+1)] = vv
                    else:        
                        features['{}_{}'.format(fe.name(),i+1)] = v
            else:
                raise Exception('{}: Unexpected type {}'.format(fk,fvtype))
        return features

    def convert_csv_for_terminal_test(self, csvfname, probtyp, newcsvname=None):
        descArr = ['_', 'BtL', 'WtK']
        probDesc = descArr[probtyp]
        if newcsvname==None:
            newcsvname = csvfname+'.t'+probDesc
        with open(csvfname, 'r') as csvfile, open(newcsvname,'w') as csvout:
            rdr = csv.DictReader(csvfile)
      
            headers = FeatureExtractor().sort_headers(rdr.fieldnames)
            wtr = csv.DictWriter(csvout, fieldnames=headers+['OUTCOME'], lineterminator='\n')
            wtr.writeheader()
            for row in rdr:
                #print('{}.{}.{}'.format(row['_DI'],row['_PROBID'],row['_MOVE']))
                pt = row['_PT']
                if pt==str(probtyp):
                    # Black-to-live; move for black
                    if probtyp==1:
                        if row['ColorFeature']=='1':
                            outcome = int(row['_SOLUTION'])*int(row['_TERM']) 
                        else:
                            outcome = '0'
                    # White-to-kill
                    elif probtyp==2:
                        if row['ColorFeature']=='0':
                            outcome = int(row['_SOLUTION'])*int(row['_TERM']) 
                        else:
                            outcome = '0'
                    # ?-to-? 
                    else:
                        outcome = int(row['_SOLUTION'])*int(row['_TERM'])

                    newrow = {h: float(row[h]) for h in headers}
                    if 'OUTCOME' not in headers:
                        newrow['OUTCOME']= outcome
                    elif(outcome != row['OUTCOME']):
                        raise ValueError('{}.{}.{}: Outcomes don''t match.'.format(row['_DI'],row['_PROBID'],row['_MOVE']))
                    wtr.writerow(newrow)
        return newcsvname    
    
    def convert_csv_for_probtype(self, csvfname, probtyp):
        newcsvname = csvfname+'.'+str(probtyp)
        with open(csvfname, 'r') as csvfile, open(newcsvname,'w') as csvout:
            rdr = csv.DictReader(csvfile)
      
            headers = FeatureExtractor().sort_headers(rdr.fieldnames)
            wtr = csv.DictWriter(csvout, fieldnames=headers+['OUTCOME'], lineterminator='\n')
            wtr.writeheader()
            for row in rdr:
                #print('{}.{}.{}'.format(row['_DI'],row['_PROBID'],row['_MOVE']))
                pt = row['_PT']
                if pt==str(probtyp):
                    # Black-to-live; move for black
                    if probtyp==1:
                        if row['ColorFeature']=='1':
                            outcome = row['_SOLUTION'] 
                        else:
                            outcome = '0'
                    # White-to-kill
                    elif probtyp==2:
                        if row['ColorFeature']=='0':
                            outcome = row['_SOLUTION']
                        else:
                            outcome = '0'
                    # ?-to-? 
                    else:
                        outcome = row['_SOLUTION']

                    newrow = {h: float(row[h]) for h in headers}
                    if 'OUTCOME' not in headers:
                        newrow['OUTCOME']= outcome
                    elif(outcome != row['OUTCOME']):
                        raise ValueError('{}.{}.{}: Outcomes don''t match.'.format(row['_DI'],row['_PROBID'],row['_MOVE']))
                    wtr.writerow(newrow)
        return newcsvname
'''
csvfname = 'c:/users/jblackmore/documents/development/rutgers/gold/problems/resplit/trainfeatures.csv'
newcsvname = 'c:/users/jblackmore/documents/development/rutgers/gold//problems/resplit/trainfeaturesBtL_T.csv'
FeatureExtractor().convert_csv_for_terminal_test(csvfname, 1, newcsvname)
csvfname = 'c:/users/jblackmore/documents/development/rutgers/gold//problems/resplit/trainfeatures.csv'
newcsvname = 'c:/users/jblackmore/documents/development/rutgers/gold//problems/resplit/trainfeaturesWtK_T.csv'
FeatureExtractor().convert_csv_for_terminal_test(csvfname, 2, newcsvname)
'''
csvfname = 'c:/users/jblackmore/documents/development/rutgers/gold/problems/resplit/devfeatures.csv'
newcsvname = 'c:/users/jblackmore/documents/development/rutgers/gold/problems/resplit/devfeaturesBtL_T.csv'
FeatureExtractor().convert_csv_for_terminal_test(csvfname, 1, newcsvname)
csvfname = 'c:/users/jblackmore/documents/development/rutgers/gold//problems/resplit/devfeatures.csv'
newcsvname = 'c:/users/jblackmore/documents/development/rutgers/gold//problems/resplit/devfeaturesWtK_T.csv'
FeatureExtractor().convert_csv_for_terminal_test(csvfname, 2, newcsvname)