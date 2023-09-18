import math
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import savgol_filter as sf

class Data:
    def __init__(self, alphaVel, normalForce, axialForce, pitchingMoment):
        self.X = alphaVel
        self.NF = normalForce
        self.AF = axialForce
        self.PM = pitchingMoment

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
    T = 296.15 # K (Found from National Weather Service website)
    p = 100914 # Pa (Also found from NWS site)
    R = 287    # J*kg^-1*K^-1
    vel = [0]*len(q)
    for i in range(0,len(q)):
        vel[i] = math.sqrt((2*abs(q[i])*R*T)/p)
    
    return vel

def datasplit(data: list):
    '''This function splits dataframe into: Alpha/Velocity, Normal Force,
    Axial Force, and Pitching Moment. Also converts forces into metric.'''
    n = 5
    lbf2N = 4.44822         # Conversion for lbf to N
    inlbs2Nm = 0.1129848333 # Conversion for in*lbf to N*m
    
    list = [0]*n
    list[0] = Data(
        data[0]['Alpha'],
        data[0]['NF/SF']*lbf2N,
        data[0]['AF/AF2']*lbf2N,
        data[0]['PM/YM']*inlbs2Nm
    )
    
    for i in range(1,n):
        list[i] = Data(
            q2v(data[i]['q']),
            data[i]['NF/SF']*lbf2N,
            data[i]['AF/AF2']*lbf2N,
            data[i]['PM/YM']*inlbs2Nm
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
fig3, [ax3, ax4] = plt.subplots(2)

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
ax4.set_xlabel('Alpha [deg]')
ax4.set_ylabel('Axial Force [N]')
ax4.plot(
    sf(flatPlateAng.X, wl, po),
    sf(flatPlateAng.AF, wl, po),
    'b-',
    label='Axial Force'
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
plt.show()