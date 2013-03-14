'''
Created on Mar 4, 2013

@author: Supun Jayathilake(supunj@gmail.com)
'''

import re
from decimal import Decimal

class PolishUtil(object):
    '''
    Utilities related to polish format
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    # Find max road and no ids
    def findMaxNodandRoadId(self, mp_file):
        dictionary = dict(RoadID=Decimal('0'), Nod=Decimal('0'))
        
        for line in mp_file:
            if line.startswith('RoadID') or re.match(r'^(Nod\d+)', line, flags=0):
                key_value = line.split('=');
                
                if line.startswith('Nod'):
                    # Get only the Nod part for the key
                    key = ''.join([i for i in key_value[0] if i.isalpha()])
                    # Nod1=0,27530,0
                    val = key_value[1].strip().split(',')[1]
                # If it is road id
                else:
                    key = key_value[0]
                    val = key_value[1].strip()
                
                # Current value stored in the dictionary
                current_val = dictionary[key]
                
                # If it is the first value just put it in the dictionary
                dictionary[key] = max(Decimal(val), current_val)
                
        
        # Go back to the beginning of the file
        mp_file.seek(0)
        
        return dictionary
