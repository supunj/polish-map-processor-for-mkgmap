'''
Created on Mar 3, 2013

@author: Supun Jayathilake(supunj@gmail.com)
'''
import collections
from multiprocessing.dummy import dict
from polish.util.polishutil import PolishUtil

class Shape:
       
    _Type = ''
    _Label = ''
    _EndLevel = ''
    _Marine = ''
    _Data = None
    
    # All polish utilities - This will act as a static
    polish_util = PolishUtil()

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
        self._Data[key] = value.replace('),(', ')^(').split('^')

    Type = property(get_type, set_type, None, None)
    Label = property(get_label, set_label, None, None)
    EndLevel = property(get_end_level, set_end_level, None, None)
    Marine = property(get_marine, set_marine, None, None)


class Polyline(Shape):
   
    ROUTABLE_TYPES = ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', '0x8', 
                      '0x9', '0xa', '0xb', '0xc', '0x14', '0x16', '0x1a', '0x1b']
    
    ROAD_BOARD_MAP = {'0x1' : '~[0x04]',
                      '0x2' : '~[0x02]',
                      '0x3' : '~[0x03]'}
    
    _RoadID = ''
    _DirIndicator = ''
    _RouteParam = ''
    _Nod = None
    _split_roads = None
    
    def __init__(self):
        super().__init__()
        self._Nod = dict()
        self._split_roads = list()


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
            numberofData = len(self._Data[0])
            
            # Add a Nod for every nod_frequency data
            for i in range(0, numberofData, nod_frequency):
                #Check if Nod already exists            
                if i in self._Nod.keys():
                    continue
                else:
                    max_nod_id += 1
                    self._Nod[int(i)] = str(i) + ',' + str(max_nod_id) + ',' + '0'
                
        return max_nod_id
    
    # Add boards to roads
    def addRoadBoards(self):
        if self.isRoutable() and self.Type in self.ROAD_BOARD_MAP:
            self.Label = self.ROAD_BOARD_MAP[self.Type] + self.Label
    
    # Split road from Nods
    def splitRoadfromNods(self, max_road_id):
        # No need to split roads with just 2 nods or less
        if len(self._Nod) <= 2:
            self._split_roads.append(self)
        else:
            new_road_data_array = list()
            
            # Get the nods in pairs
            nod_pairs = self.polish_util.pairwise(sorted(self._Nod.keys()))
            
            # Traverse through the nods
            for nod_pair in nod_pairs:
                # Clone the road and add a new road id
                new_road = self.clone()
                max_road_id+=1
                new_road.RoadID = str(max_road_id)
                
                # If the array is not empty, clear
                if len(new_road_data_array) != 0:
                    new_road_data_array.clear()
                    
                # Load a relevant data set between two nods
                for position in range(nod_pair[0], nod_pair[1]+1):
                    new_road_data_array.append(self._Data[0][position])
                
                # Set new nod and data to the new road
                nod0_value_set = self._Nod[nod_pair[0]].split(',')
                nod1_value_set = self._Nod[nod_pair[1]].split(',')
                new_road.set_data(0, ','.join(new_road_data_array))
                new_road.set_nod(0, '0,' + nod0_value_set[1] + ',' + nod0_value_set[2])
                new_road.set_nod(len(new_road_data_array)-1, str(len(new_road_data_array)-1) + ',' + nod1_value_set[1] + ',' + nod1_value_set[2])
            
                # Add the new road to the list
                self._split_roads.append(new_road)

        return self._split_roads, max_road_id
        
                                
    # Build and return the new segment
    def buildPolyline(self):
        segment = list()
        segment.append('[POLYLINE]\n')
        segment.append('Type=' + self.Type + '\n')
        segment.append('Label=' + self.Label + '\n')
        segment.append('EndLevel=' + self.EndLevel + '\n')
        if self.DirIndicator != '' : segment.append('DirIndicator=' + self.DirIndicator + '\n')
        if self.RoadID != '' : segment.append('RoadID=' + self.RoadID + '\n')
        if self.RouteParam != '' : segment.append('RouteParam=' + self.RouteParam + '\n')
        
        # Append Data
        for key, value in collections.OrderedDict(sorted(self._Data.items())).items():
            segment.append('Data' + str(key) + '=' + ','.join(value) + '\n')
            
        # Append Nod
        i = 1
        for key, value in collections.OrderedDict(sorted(self._Nod.items())).items():
            segment.append('Nod' + str(i) + '=' + value + '\n')
            i+=1
        
        segment.append('Marine=' + self.Marine + '\n')
        segment.append('[END]\n\n')
        return segment
    
    # Clone the object clearing Data and Nods
    def clone(self):
        cloned = Polyline()
        cloned.Type = self.Type
        cloned.Label = self.Label
        cloned.EndLevel = self.EndLevel
        cloned.Marine = self.Marine
        cloned.DirIndicator = self.DirIndicator
        cloned.RouteParam = self.RouteParam
        return cloned
            
class Polygon(Shape):
  
    def __init__(self):
        super().__init__()
        
        
        
class Point(Shape):
   
    def __init__(self):
        super().__init__()
        
class Restriction():

    _Nod = None
    _TraffPoints_From = None
    _TraffPoints_To = None
    _TraffRoads_From = None
    _TraffRoads_To = None
    _Time = None
    
    def get_time(self):
        return self.__Time

    def set_time(self, value):
        self.__Time = value
    
    def get_nod(self):
        return self.__Nod


    def get_traff_points_from(self):
        return self.__TraffPoints_From


    def get_traff_points_to(self):
        return self.__TraffPoints_To


    def get_traff_roads_from(self):
        return self.__TraffRoads_From


    def get_traff_roads_to(self):
        return self.__TraffRoads_To


    def set_nod(self, value):
        self.__Nod = value


    def set_traff_points_from(self, value):
        self.__TraffPoints_From = value


    def set_traff_points_to(self, value):
        self.__TraffPoints_To = value


    def set_traff_roads_from(self, value):
        self.__TraffRoads_From = value


    def set_traff_roads_to(self, value):
        self.__TraffRoads_To = value
    
    Nod = property(get_nod, set_nod, None, None)
    TraffPoints_From = property(get_traff_points_from, set_traff_points_from, None, None)
    TraffPoints_To = property(get_traff_points_to, set_traff_points_to, None, None)
    TraffRoads_From = property(get_traff_roads_from, set_traff_roads_from, None, None)
    TraffRoads_To = property(get_traff_roads_to, set_traff_roads_to, None, None)
    Time = property(get_time, set_time, None, None)
    
    # Build the restriction
    def buildRestriction(self):
        segment = list()
        segment.append('[Restrict]\n')
        segment.append('Nod=' + self.Nod + '\n')
        segment.append('TraffPoints=' + self.TraffPoints_From + ',' + self.Nod + ',' + self.TraffPoints_To + '\n')
        segment.append('TraffRoads=' + self.TraffRoads_From + ',' + self.TraffRoads_To + '\n')
        segment.append('Time=' + self.Time + '\n')
        segment.append('[END-Restrict]\n\n')
        return segment
