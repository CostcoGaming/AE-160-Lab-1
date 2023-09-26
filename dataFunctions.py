import math
import pandas as pd
from scipy.optimize import curve_fit as cf
import numpy as np

# Create global variables
global psf2pa
psf2pa = 0.020885 # Conversion factor for psf --> Pa

# ------------------------------------------------------------------------------
# ---------------------------- Classes & Functions -----------------------------
# ------------------------------------------------------------------------------

# Create object in order to call specific property of data rather than use messy
# and confusing list formatting
class Data:
    def __init__(self, alphaVel, normalForce, axialForce, pitchingMoment,
                 coefficientLift, coefficientDrag):
        self.X = alphaVel # Either AoA or v_inf
        self.NF = normalForce
        self.AF = axialForce
        self.PM = pitchingMoment
        self.CL = coefficientLift
        self.CD = coefficientDrag

def read_files(files:list[str]):
    '''This function reads .csv a list of files and turns it into a list of 
    pandas dataframes'''
    
    n = len(files)
    new_files = [0]*n
    rows = [0,1,2,3,4,5,6,8] # Skips these rows when reading csv files

    # Iterate through list of strings to read .csv files
    for i in range(0,n):
        new_files[i] = pd.read_csv(files[i], skiprows=rows)

    return new_files

def q2v(q:list[int]):
    '''This function uses the ideal gas law and the dynamic pressure equation
    in order to convert dynamic pressure into wind velocity'''
    T = 296.15        # K (Found from National Weather Service website)
    p = 100914        # Pa (Also found from NWS site)
    R = 287           # J*kg^-1*K^-1 (Specific gas constant for air)
    
    n = len(q)
    vel = [0]*n
    for i in range(0,n):
        # use absolute value of q so as not to get a domain error w/ sqrt
        vel[i] = math.sqrt((2*abs(q[i]/psf2pa)*R*T)/p)
    
    return vel

def force2coeff(force:list[int], q:list[int], S:int):
    '''This function converts force into its corresponding coefficients 
    (i.e, lift force --> coefficient of lift)'''
    n = len(force)
    coefficient = [0]*n # Initializing list

    # Iterate through force & q in order to find coefficients.
    for i in range(0,n):
        if q[i] == 0: # Skips when q = 0, so as not to divide by 0.
            coefficient[i] = None
        else:
            coefficient[i] = force[i]/(q[i]*S)
        
    return coefficient

def moment2coeff(moment:list[int], q:list[int], S:list[int]):
    '''This functions converts pitching moment into its corresponding pitching
    moment coefficient.'''
    
    n = len(moment)
    coefficient = [0]*n # Initializing list
    
    # Iterate through moments 

    return

def NA2LD(N:list[int], A:list[int], alphaDeg:list[int]):
    '''This function takes normal/axial force and angle of attack and converts
    it into lift/drag force'''
    
    n = len(N)

    # Initialize lists
    liftForce = [0]*n
    dragForce = liftForce
    alphaRad = liftForce

    # Iterate through list to convert to lift force for corresponding
    # normal/axial forces + AoA.
    for i in range(0,n):
        alphaRad[i] = math.radians(alphaDeg[i]) # Convert AoA into radians
        liftForce[i] = N[i]*math.cos(alphaRad[i]) - A[i]*math.sin(alphaRad[i])
        dragForce[i] = N[i]*math.sin(alphaRad[i]) + A[i]*math.cos(alphaRad[i])

    return liftForce, dragForce

def moment_transfer(moment:list[int], normal:list[int], b:list[int]):
    A = 28.829/1000 # m
    D = 71.04/1000 # m
    n = len(moment)
    C = D-b    

    new_moment = [0]*n
    
    for i in range(0,n):
        new_moment[i] = moment[i] - (A + C)*normal[i]
        
    return new_moment

def AF_Curve(x, a, b, c):
    return a*x**2 + b*x + c

def get_AF_curve(x, y):
    popt, _ = cf(AF_Curve, x, y)

    a, b, c = popt

    x_line = np.arange(min(x), max(x))
    y_line = AF_Curve(x_line, a, b, c)

    return [x_line, y_line, a, b, c]

def aoa_curve(x, a, b):
    return a*x + b

def get_aoa_curve(x, y):
    popt, _ = cf(aoa_curve, x, y)
    
    a, b = popt
    
    x_line = np.arange(min(x), max(x))
    y_line = aoa_curve(x_line, a, b)
    
    return [x_line, y_line, a, b]

def coeff_curve(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

def get_coeff_curve(x, y):
    popt, _ = cf(coeff_curve, x, y)
    
    a, b, c, d = popt
    
    x_line = np.arange(min(x), max(x))
    y_line = coeff_curve(x_line, a, b, c, d)
    
    return [x_line, y_line, a, b, c, d]

def data_split(data:list):
    '''This function splits dataframe into: Alpha/Velocity, Normal Force,
    Axial Force, and Pitching Moment. Also converts forces into metric.'''
    
    diameters = [ # Diameters in mm
        74.82, # Flat Plate
        74.82, # Flat Plate
        74.82, # Flat Plate
        75.48, # Half Sphere
        75.40, # Inverted Cup
        76.21  # Sphere
    ]

    B = [       # B Value in mm
        98.42,  # Flat Plate 
        98.42,  # Flat Plate 
        98.42,  # Flat Plate
        99.27,  # Half Sphere
        127.00, # Inverted Cup
        146.92, # Sphere
    ]

    diameters[:] = [x/1000 for x in diameters] # Convert to m
    B[:] = [x/1000 for x in B] # Convert to m

    lbf2N = 4.44822         # Conversion for lbf to N
    inlbs2Nm = 0.1129848333 # Conversion for in*lbf to N*m
    n = len(data)

    # Find lifting force and drag force based on AoA and normal/axial forces.
    # Only for flat plate angle
    lF0, dF0 = NA2LD(data[0]['NF/SF']*lbf2N, data[0]['AF/AF2']*lbf2N,
                   data[0]['Alpha'])
    lF, dF = NA2LD(data[1]['NF/SF']*lbf2N, data[1]['AF/AF2']*lbf2N,
                   data[1]['Alpha'])
    
    # Separate Flat Plate Angle from other data, since x axis will be AoA
    # rather than wind velocity.
    
    list = [0]*n
    list[0] = Data(
        data[0]['Alpha'],
        data[0]['NF/SF']*lbf2N,
        data[0]['AF/AF2']*lbf2N,
        data[0]['PM/YM']*inlbs2Nm,
        force2coeff(lF0, data[0]['q']/psf2pa, diameters[0]),
        force2coeff(dF0, data[0]['q']/psf2pa, diameters[0])
    )
    
    list[0].PM = moment_transfer(list[0].PM, list[0].NF, B[0])

    list[1] = Data(
        data[1]['Alpha'],
        data[1]['NF/SF']*lbf2N,
        data[1]['AF/AF2']*lbf2N,
        data[1]['PM/YM']*inlbs2Nm,
        force2coeff(lF, data[1]['q']/psf2pa, diameters[1]),
        force2coeff(dF, data[1]['q']/psf2pa, diameters[1])
    )
    
    list[1].PM = moment_transfer(list[1].PM, list[1].NF, B[1])
    
    # Iterate through data to split for each shape and assign different types of
    # data to object properties.
    for i in range(2,n):
        list[i] = Data( # Assume NF/AF == LF/DF since AoA = 0
            q2v(data[i]['q']),         # convert 'q' column into v_inf
            data[i]['NF/SF']*lbf2N,    # Normal Force
            data[i]['AF/AF2']*lbf2N,   # Axial Force
            data[i]['PM/YM']*inlbs2Nm, # Pitching Moment
            force2coeff(data[i]['NF/SF']*lbf2N, data[i]['q']/psf2pa, diameters[i]),
            force2coeff(data[i]['AF/AF2']*lbf2N, data[i]['q']/psf2pa, diameters[i])
        )   
        list[i].PM = moment_transfer(list[i].PM, list[i].NF, B[i])

    return list
