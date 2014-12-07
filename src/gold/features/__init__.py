from gold.features.ColorFeature import ColorFeature
from gold.features.DiffLiberties import DiffLiberties
from gold.features.DistanceFromCenterFeature import DistanceFromCenterFeature
from gold.features.StoneCountFeature import StoneCountFeature
from gold.features.numberLiveGroups import numberLiveGroups
from gold.features.LocalShapesFeature import LocalShapesFeature
from gold.features.PatchExtractor import PatchExtractor
from gold.features.SparseDictionaryFeature import SparseDictionaryFeature
from gold.features.HuMomentsFeature import HuMomentsFeature
from gold.features.Feature import Feature

FEATURE_SERVICES = ['ColorFeature', 'StoneCountFeature', 'DiffLiberties',  
                    'DistanceFromCenterFeature', 'numberLiveGroups', 'HuMomentsFeature',
                    'LocalShapesFeature', 'SparseDictionaryFeature']

__all__ = FEATURE_SERVICES + ['Feature', 'FEATURE_SERVICES']