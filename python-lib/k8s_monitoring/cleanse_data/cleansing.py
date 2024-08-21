def cleanse_cpu(v):
    """
    # Convert all CPU values into 1 single unit
    """
    # Return 0 on None/0/'None'
    if (v == 0) or (not v) or (v  == 'None'):
        return 0
    
    # Try to convert to INT
    try:
        v = int(v)
    except:
        pass
    
    # Convert str values from 'n' or 'm'
    if type(v) == str:
        unit = v[-1].lower()
        if unit not in ['n', 'c', 'm', 'u']:
            raise Exception(f'ERROR - Unit type not found :: {v}')
        
        # U = Greek mu == C
        # M = Mili  = 1CPU = 1,000
        # C = Centi = 1CPU = 1,000,000
        # N = Nano  = 1CPU = 1,000,000,000
        v = int(v[0:-1])
        v = v * 1000
        if unit == 'u':
            v = round(v / 1000000, 0)
        elif unit == 'm':
            v = round(v / 1000, 0)
        elif unit == 'c':
            v = round(v / 1000000, 0)
        elif unit == 'n':
            v = round(v / 1000000000, 0)
        else:
            raise Exception(f'ERROR - Could not convert unit :: {unit} / {v}')
            
    # Normal ints, seem to be the 'cpu' core count, convert to 'm'
    elif type(v) == int:
        v = int(v)
        if v == -1:
            v = -1
        else:
            v *= 1000
    
    # Return v
    return v


def cleanse_memory(v):
    """
    # Convert everything to "Kibibyte::1024" or "Kilobyte::1000"
    """
    d = {
        'Ki': 1,
        'Kb': 1,
        'Mi': 1024,
        'Mb': 1000,
        'Gi': 1024000,
        'Gb': 1000000
    }
    try:
        suffix = v[-2:]
        v = int(v[:-2])
        v *= d[suffix]
    except:
        v = 0    
    return v



def compute_percent(v):
    """
    # Compute percentage
    """
    if (not v[0]) or (not v[1]):
        return 0
    
    x = v[0]
    if type(x) == str:
        x = ''.join([i for i in x if not i.isalpha()])
        x = int(x)
    
    y = v[1]
    if type(y) == str:
        y = ''.join([i for i in y if not i.isalpha()])
        y = int(y)
        
    if (x == 0) or (y == 0):
        return 0

    z = round(y/x*100, 2)
    return z

# EOF