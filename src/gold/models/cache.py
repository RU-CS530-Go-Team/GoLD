'''
Created on Dec 12, 2014

@author: JBlackmore
'''
from time import clock

MAXNODES=1000000
class Cache(object):
    '''
    classdocs
    '''

    maxnodes = MAXNODES
    cache = {}
    keys = []
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def clear(self):
        Cache.cache = {}
        Cache.keys = []
    
    def evict_oldest_nodes(self):
        if len(Cache.cache.keys())<Cache.maxnodes:
            return Cache.cache
        # Try evicting oldest 2%
        evict_count = int(Cache.maxnodes/50)
        nodes_evicted=0
        while nodes_evicted<evict_count:
            try:
                Cache.cache.remove(Cache.keys.pop(Cache.keys.index(False)))
            except Exception:
                Cache.cache.remove(Cache.keys.pop(0))
            nodes_evicted+=1
        return Cache.cache
    
    def put(self, key, value):
        try:
            # Make sure we don't expire same key if 
            # we saw it before
            i=0
            while i>=0:
                i=Cache.keys.index(key)
                Cache.keys.remove(i)
        except Exception:
            pass
        Cache.cache[key] = value
        Cache.keys.append(key)
        self.evict_oldest_nodes()
    
    def get(self, key):
        
        try:
            value = Cache.cache[key]
            index = Cache.keys.index(key)
            Cache.keys.pop(index)
            Cache.keys.append(key)
            return value
        except KeyError:
            return None
