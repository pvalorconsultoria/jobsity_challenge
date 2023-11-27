import numpy as np
import re

def parse_point(point_str):
    regex = r"POINT \((.*) (.*)\)"
    result = re.search(regex, point_str)
    
    if result:
        coord_x = np.float64(result.group(1))
        coord_y = np.float64(result.group(2))

        return coord_x, coord_y
    else:
        return np.nan, np.nan