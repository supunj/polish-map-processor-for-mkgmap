'''
Created on Mar 3, 2013

@author: Supun Jayathilake(supunj@gmail.com)
'''
from decimal import Decimal
from multiprocessing.dummy import dict

class Shape:
    '''
    classdocs
    '''
    
    _Type = ''
    _Label = ''
    _EndLevel = ''
    _Marine = ''
    _Data = None

    def __init__(self):
        self._Data = dict()

    def get_type(self):
        return self.__Type


    def get_label(self):
        return self.__Label


    def get_end_level(self):
        return self.__EndLevel


    def get_marine(self):
        return self.__Marine


    def set_type(self, value):
        self.__Type = value


    def set_label(self, value):
        self.__Label = value


    def set_end_level(self, value):
        self.__EndLevel = value


    def set_marine(self, value):
        self.__Marine = value
        
    def get_data(self, key):
        if key not in self._Data.keys():
            raise KeyError
    
        return self._Data[key]
    
    def set_data(self, key, value):
        self._Data[key] = value

    Type = property(get_type, set_type, None, None)
    Label = property(get_label, set_label, None, None)
    EndLevel = property(get_end_level, set_end_level, None, None)
    Marine = property(get_marine, set_marine, None, None)



class Polyline(Shape):
    '''
    classdocs
    '''
    ROUTABLE_TYPES = ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', '0x8', 
                      '0x9', '0xa', '0xb', '0xc', '0x14', '0x16', '0x1a', '0x1b']
    
    ROAD_BOARD_MAP = {'0x1' : '~[0x04]',
                      '0x2' : '~[0x02]',
                      '0x3' : '~[0x03]'}
    
    _RoadID = ''
    _DirIndicator = ''
    _RouteParam = ''
    _Nod = None
    
    def __init__(self):
        super().__init__()
        self._Nod = dict()


    def get_nod(self, key):
        if key not in self._Data.keys():
            raise KeyError
        
        return self._Nod[key]


    def set_nod(self, key, value):
        self._Nod[key] = value


    def get_road_id(self):
        return self.__RoadID


    def get_dir_indicator(self):
        return self.__DirIndicator


    def get_route_param(self):
        return self.__RouteParam


    def set_road_id(self, value):
        self.__RoadID = value


    def set_dir_indicator(self, value):
        self.__DirIndicator = value


    def set_route_param(self, value):
        self.__RouteParam = value
    
    # Check if the line is a routable type    
    def isRoutable(self):
        if self.Type in self.ROUTABLE_TYPES:
            return True
        else:
            return False

    RoadID = property(get_road_id, set_road_id, None, None)
    DirIndicator = property(get_dir_indicator, set_dir_indicator, None, None)
    RouteParam = property(get_route_param, set_route_param, None, None)
        
    # Add additional Nods
    def addAdditionalNods(self, max_nod_id, nod_frequency):
        # Do this only for the routable Polylines
        if self.isRoutable():
            numberofData = len(self._Data['Data0'].split('),('))
            
            # Traverse through the Nod dictionary and find the max Nod and Nod ids
            next_nod_number = 0
            existing_nods = []
            for key, value in self._Nod.items():
                next_nod_number = max(Decimal(''.join([i for i in key if i.isnumeric()])), Decimal(next_nod_number))
                existing_nods.append(value.strip().split(',')[0])
            
            # Add a Nod for every nod_frequency data
            for i in range(0, numberofData, nod_frequency):
                #Check if Nod already exists            
                if str(i) in existing_nods:
                    continue
                else:
                    max_nod_id += 1
                    next_nod_number += 1
                    self._Nod['Nod' + str(next_nod_number)] = str(i) + ',' + str(max_nod_id) + ',' + '0'
                
        return max_nod_id
    
    # Add boards to roads
    def addRoadBoards(self):
        if self.Type in self.ROAD_BOARD_MAP:
            self.Label = self.ROAD_BOARD_MAP[self.Type] + self.Label
                                
    # Build and return the new segment
    def buildPolyline(self):
        segment = []
        segment.append('[POLYLINE]\n')
        segment.append('Type=' + self.Type + '\n')
        segment.append('Label=' + self.Label + '\n')
        segment.append('EndLevel=' + self.EndLevel + '\n')
        if self.DirIndicator != '' : segment.append('DirIndicator=' + self.DirIndicator + '\n')
        if self.RoadID != '' : segment.append('RoadID=' + self.RoadID + '\n')
        if self.RouteParam != '' : segment.append('RouteParam=' + self.RouteParam + '\n')
        
        # Append Data
        for key, value in self._Data.items():
            segment.append(key + '=' + value + '\n')
            
        # Append Nod
        for key, value in self._Nod.items():
            segment.append(key + '=' + value + '\n')
        
        segment.append('Marine=' + self.Marine + '\n')
        segment.append('[END]\n\n')
        return segment
            
class Polygon(Shape):
    '''
    classdocs
    '''


    def __init__(self):
        super().__init__()
        
        
        
class Point(Shape):
    '''
    classdocs
    '''


    def __init__(self):
        super().__init__()
