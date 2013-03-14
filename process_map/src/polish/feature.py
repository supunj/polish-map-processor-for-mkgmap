'''
Created on Mar 4, 2013

@author: SupunJ
'''

import re
from polish.element import Polyline

class FeatureHandler():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
    # Return all segment contents in a dictionary
    def _getSegmentinDictionary(self, segment_contents):
        d = dict()
        for line in segment_contents:            
            if not (line.startswith('[') or line.startswith('\n')):
                key_val = line.strip().split('=', maxsplit=1)
                d[key_val[0]] = key_val[1]
                
        return d
    
    # Handle common attributes in each segment
    def _handle_Common(self, segment_dict, shape):
        shape.Type = segment_dict.get('Type', '0x0')
        shape.Label = segment_dict.get('Label', '')
        shape.EndLevel = segment_dict.get('EndLevel', '2')
        shape.Marine = segment_dict.get('Marine', 'N')
        
        # Add all Data elements
        for key, value in segment_dict.items():
            if re.match(r'^(Data\d+)', key, flags=0):
                shape.set_data(key, value)
         
    # Handle the IMG_ID segment
    def handle_IMG_ID(self, segment_contents):
        return ''.join(segment_contents)
    
    # Handle the POLYLINE segment
    def handle_POLYLINE(self, segment_contents, max_nod_id, max_road_id, nod_frequency):
        polyLine = Polyline()
        
        # Get all segment contents in a dictionary
        segment_dict = self._getSegmentinDictionary(segment_contents);
        
        # Add common contents
        self._handle_Common(segment_dict, polyLine)
        
        # Add specific contents
        polyLine.RoadID = segment_dict.get('RoadID', '')
        polyLine.DirIndicator = segment_dict.get('DirIndicator', '')
        polyLine.RouteParam = segment_dict.get('RouteParam', '')
       
        # Add all Nod elements
        for key, value in segment_dict.items():
            if re.match(r'^(Nod\d+)', key, flags=0):
                polyLine.set_nod(key, value)
        
        # Generate additional routing nodes
        new_max_nod_id = polyLine.addAdditionalNods(max_nod_id, nod_frequency)
     
        # Add road boards to key types of roads
        polyLine.addRoadBoards()
        
        return ''.join(polyLine.buildPolyline()), new_max_nod_id, max_road_id
    
    
    # Handle the POI segment
    def handle_POI(self, segment_contents):
        return ''.join(segment_contents)
    
    # Handle the POLYGON segment
    def handle_POLYGON(self, segment_contents):
        return ''.join(segment_contents)
    
    # Handle the Restrict segment
    def handle_Restrict(self, segment_contents):
        return ''.join(segment_contents)