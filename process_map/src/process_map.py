'''
Created on Mar 3, 2013

@author: Supun Jayathilake(supunj@gmail.com)
'''

import sys
import re
from polish.util.polishutil import PolishUtil
from polish.feature import FeatureHandler
from decimal import Decimal
from exception.custom_exceptions import ProgramParamException

if __name__ == '__main__':
    try:
        # Check if all required parameters are supplied or not
        if sys.argv[1] == None or sys.argv[2] == None or sys.argv[3] == None:
            raise ProgramParamException
        
        # List that keeps values that needs to be written to new mp file.
        out_list = list()
        
        # Keeps the turn restrictions list
        turn_restrictions = list()
        
        # Open the input mp
        input_mp = open(sys.argv[1])
        
        # All polish utilities
        polish_util = PolishUtil()
        
        # Feature handler
        feature_handler = FeatureHandler()
        
        # Get the max values for road and nod ids
        max_values = polish_util.findMaxNodandRoadId(input_mp)
        print("Max values -> " + str(max_values))
        
        # Global Nod to Road map dictionary
        nod_to_roads = dict()
        
        # Open the output mp to write
        output_mp = open(sys.argv[2], 'w')
        
        # Specifies the frequency the routing nods should be added
        nod_frequency = int(sys.argv[3])
        
        # Loop through the lines
        is_segment = False
        current_feature = None
        for line in input_mp:
            # Collect only the lines that matters
            if line.startswith(';') or line == '\n':
                continue
            else:
                out_list.append(line);
            
            if re.match(r'\[(IMG ID|Restrict|POI|POLYLINE|POLYGON)\]', line, flags=0):
                current_feature = line.strip()
                continue
                
            if current_feature != None and re.match(r'\[(END|END-IMG ID|END-Restrict)\]', line, flags=0):
                # Add a new line between segments  
                out_list.append('\n');
                
                if current_feature == '[IMG ID]':
                    output_mp.write(feature_handler.handle_IMG_ID(out_list))
                else:
                    if current_feature == '[POLYLINE]':
                        segment_strings, new_max_nod_id, new_max_road_id  = feature_handler.handle_POLYLINE(out_list, max_values['Nod'], max_values['RoadID'], nod_frequency)
                        max_values['Nod'] = Decimal(new_max_nod_id)
                        max_values['RoadID'] = Decimal(new_max_road_id)
                        
                        for segment_string in segment_strings:
                            output_mp.write(segment_string)
                    else:
                        if current_feature == '[POI]':
                            output_mp.write(feature_handler.handle_POI(out_list))
                        else:
                            if current_feature == '[POLYGON]':
                                output_mp.write(feature_handler.handle_POLYGON(out_list))
                            else:
                                if current_feature == '[Restrict]':
                                    turn_restrictions.append(feature_handler.handle_Restrict(out_list))
                
                # Clear segment
                out_list.clear()
                current_feature = None
                
        # Write turn restrictions
        for turn_rest in turn_restrictions:
            output_mp.write(''.join(turn_rest.buildRestriction()))
        
    except FileNotFoundError:
        print("Provided file was not found")
    except ProgramParamException:
        print("Please provide both the input/output files and the routing node frequency.")
    finally:
        # Close all open files
        input_mp.close()
        output_mp.close()
    