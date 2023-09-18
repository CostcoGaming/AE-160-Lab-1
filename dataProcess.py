import math
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import savgol_filter as sf

# Create global variables
global T, p, R, psf2pa
T = 296.15        # K (Found from National Weather Service website)
p = 100914        # Pa (Also found from NWS site)
R = 287           # J*kg^-1*K^-1 (Specific gas constant for air)
psf2pa = 0.020885 # Converts psf into Pa

class Data:
    def __init__(self, alphaVel, normalForce, axialForce, pitchingMoment,
                 coefficientLift, coefficientDrag):
        self.X = alphaVel
        self.NF = normalForce
        self.AF = axialForce
        self.PM = pitchingMoment
        self.CL = coefficientLift
        self.CD = coefficientDrag

def read_files(files: list[str]):
    '''This function reads .csv a list of files and turns it into a list of 
    pandas dataframes'''
    
    new_files = [0]*len(files)
    rows = [0,1,2,3,4,5,6,8] # Skips these rows when reading csv files
    for i in range(0,len(files)):
        new_files[i] = pd.read_csv(files[i], skiprows=rows)

    return new_files

def q2v(q: list):
    '''This function uses the ideal gas law and the dynamic pressure equation
    in order to convert dynamic pressure into wind velocity'''
    
    vel = [0]*len(q)
    for i in range(0,len(q)):
        vel[i] = math.sqrt((2*abs(q[i]/psf2pa)*R*T)/p)
    
    return vel

def force2coeff(force: list, q: list):
    '''This function converts force into coefficients (i.e, lift force --> 
    coefficient of lift)'''
    n = len(force)
    S = 0.01 # m (Length of object)
    
    coefficient = [0]*n
    for i in range(0,n):
        if q[i] == 0: # Skips when q = 0, so as not to divide by 0.
            coefficient[i] = None
        else:
            coefficient[i] = force[i]/(q[i]*S)
        
    return coefficient

def NA2LD(N:list, A:list, alphaDeg: list):
    '''This function takes normal/axial force and angle of attack and converts
    it into lift/drag force'''
    
    n = len(N)
    liftForce = [0]*n
    dragForce = liftForce
    alphaRad = liftForce
    for i in range(0,n):
        alphaRad[i] = math.radians(alphaDeg[i]) # Convert AoA into radians
        liftForce[i] = N[i]*math.cos(alphaRad[i]) - A[i]*math.sin(alphaRad[i])
        dragForce[i] = N[i]*math.sin(alphaRad[i]) + A[i]*math.cos(alphaRad[i])

    return liftForce, dragForce

def datasplit(data: list):
    '''This function splits dataframe into: Alpha/Velocity, Normal Force,
    Axial Force, and Pitching Moment. Also converts forces into metric.'''
    
    lbf2N = 4.44822         # Conversion for lbf to N
    inlbs2Nm = 0.1129848333 # Conversion for in*lbf to N*m
    n = len(data)
    
    lF, dF = NA2LD(data[0]['NF/SF']*lbf2N, data[0]['AF/AF2']*lbf2N,
                   data[0]['Alpha'])
    
    list = [0]*n
    list[0] = Data(
        data[0]['Alpha'],
        data[0]['NF/SF']*lbf2N,
        data[0]['AF/AF2']*lbf2N,
        data[0]['PM/YM']*inlbs2Nm,
        force2coeff(lF, data[0]['q']/psf2pa),
        force2coeff(dF, data[0]['q']/psf2pa)
        
    )
    
    for i in range(1,n):
        list[i] = Data( # Assume NF/AF == LF/DF since AoA = 0
            q2v(data[i]['q']),
            data[i]['NF/SF']*lbf2N,
            data[i]['AF/AF2']*lbf2N,
            data[i]['PM/YM']*inlbs2Nm,
            force2coeff(data[i]['NF/SF']*lbf2N, data[i]['q']/psf2pa),
            force2coeff(data[i]['AF/AF2']*lbf2N, data[i]['q']/psf2pa)
        )   

    return list

# File reading
path = str(Path(__file__).parent)+'/Data' # Finds current path and Data folder
files = [
    path+'/Flat Plate Angle.csv',
    path+'/Flat Plate Velocity.csv',
    path+'/Half Sphere.csv',
    path+'/Inverted Cup.csv',
    path+'/Sphere.csv'
]

data = read_files(files)

flatPlateAng, flatPlateVel, halfSphere, invertedCup, sphere = datasplit(data)

# Set up window
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, [ax3, ax3_2] = plt.subplots(2)
fig4, [ax4, ax4_2] = plt.subplots(2)

# Savitsky-Golay filter coefficients
wl = 151 # Window Length
po = 2   # Polynomial Order

# Normal Force v Velocity
ax1.set_xlabel('V_inf [m/s]')
ax1.set_ylabel('Normal Force [N]')
ax1.plot(
    sf(flatPlateVel.X, wl, po),
    flatPlateVel.NF,
    'r-',
    label='Flat Plate',
    zorder=10
)
ax1.plot(
    sf(halfSphere.X, wl, po),    
    halfSphere.NF,
    'b-',
    label='Half Sphere',
    zorder=15 
)
ax1.plot(
    sf(invertedCup.X, wl, po),
    invertedCup.NF,
    'k-',
    label='Inverted Cup',
    zorder=5
)
ax1.plot(
    sf(sphere.X, wl, po),
    sphere.NF,
    'g-',
    label='Sphere',
    zorder=0
)

# Axial Force v Velocity
ax2.set_xlabel('V_inf [m/s]')
ax2.set_ylabel('Axial Force [N]')
ax2.plot(
    sf(flatPlateVel.X, wl, po),
    sf(flatPlateVel.AF, wl, po),
    'r-',
    label='Flat Plate',
    zorder=2
)
ax2.plot(
    sf(halfSphere.X, wl, po),
    sf(halfSphere.AF, wl, po),
    'b-',
    label='Half Sphere',
    zorder=5
)
ax2.plot(
    sf(invertedCup.X, wl, po),
    sf(invertedCup.AF, wl, po),
    'k-',
    label='Inverted Cup',
    zorder=10
)
ax2.plot(
    sf(sphere.X, wl, po),
    sf(sphere.AF, wl, po),
    'g-',
    label='Sphere',
    zorder=0
)

# Normal/Axial Force v Angle of Attack
ax3.set_xlabel('Alpha [deg]')
ax3.set_ylabel('Normal Force [N]')
ax3.plot(
    sf(flatPlateAng.X, wl, po),
    sf(abs(flatPlateAng.NF), wl, po),
    'r-',
    label='Normal Force'
)
ax3_2.set_xlabel('Alpha [deg]')
ax3_2.set_ylabel('Axial Force [N]')
ax3_2.plot(
    sf(flatPlateAng.X, wl, po),
    sf(flatPlateAng.AF, wl, po),
    'b-',
    label='Axial Force'
)

ax4.set_xlabel('Alpha [deg]')
ax4.set_ylabel('Lift Coefficient')
ax4.plot(
    sf(flatPlateAng.X, wl, po),
    sf(flatPlateAng.CL, wl, 1),
    'r-',
    label='Coefficient of Lift'
)
ax4_2.set_xlabel('Alpha [deg]')
ax4_2.set_ylabel('Drag Coefficient')
ax4_2.plot(
    sf(flatPlateAng.X, wl, po),
    sf(flatPlateAng.CD, wl, 1),
    'b-',
    label='Coefficient of Drag'
)

# Graph formating
ax1.set_title('Normal Force vs Free Stream Velocity')
ax1.set_xlim(xmin=0)
ax1.legend()
ax2.set_title('Axial Force vs Free Stream Velocity')
ax2.set_xlim(xmin=0)
ax2.legend()
ax3.set_title('Normal/Axial Force vs Angle of Attack')
ax3.set_xlim(xmin=0)
ax3_2.set_xlim(xmin=0)
ax4.set_title('Coefficient of Lift vs Angle of Attack')
ax4.set_xlim(xmin=0)
ax4_2.set_xlim(xmin=0)
plt.show()