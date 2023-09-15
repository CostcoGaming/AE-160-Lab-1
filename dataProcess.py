import math
import pandas as pd
import matplotlib.pyplot as plt

def read_files(files):
    new_files = [0]*len(files)
    for i in range(0,len(files)):
        new_files[i] = pd.read_csv(files[i], skiprows=[1])

    return new_files

def q2v(q, T, p):
    # This functions takes dynamic pressure, temperature, and pressure and 
    # converts it into wind speed.
    R = 287 # J*kg^-1*K^-1
    vel = [0]*len(q)
    for i in range(0,len(q)):
        vel[i] = math.sqrt((2*q[i]*R*T)/p)
    
    return vel

path = r"D:\School\'23 Fall\Lab\AE 160\Lab 1" # Desktop
# path = r"/Users/bruh/Documents/Codes/AE 160/Data" # Mac
files = [
    path+'\Flat Plate Angle.csv',
    path+'\Flat Plate Velocity.csv',
    path+'\Half Sphere.csv',
    path+'\Inverted Cup.csv',
    path+'\Sphere.csv'
]

temp = 296.15 # K (Found from National Weather Service website)
pressure = 100914 # Pa (Also found from NWS site)
data = read_files(files)

flatPlateAng = data[0]
flatPlateVel = data[1]
halfSphere = data[2]
invertedCup = data[3]
sphere = data[4]

flatPlateAngData = [
    flatPlateAng['Alpha'],               # Angle of Attack in deg
    flatPlateAng['NF/SF']*4.44822,       # Normal Force in N
    flatPlateAng['AF/AF2']*4.44822,      # Axial Force in N
    flatPlateAng['PM/YM']*0.1129848333   # Pitching Moment in N*m
]

flatPlateVelData = [
    q2v(abs(flatPlateVel['q'])/0.020885, temp, pressure), # Velocity in m/s
    flatPlateVel['NF/SF']*4.44822,                        # Normal Force in N
    flatPlateVel['AF/AF2']*4.44822,                       # Axial Force in N
    flatPlateVel['PM/YM']*0.1129848333,                   # Pitching Moment in N*m
]

halfSphereData = [
    q2v(abs(halfSphere['q'])/0.020885, temp, pressure), # Velocity in m/s
    halfSphere['NF/SF']*4.44822,                        # Normal Force in N
    halfSphere['AF/AF2']*4.44822,                       # Axial Force in N
    halfSphere['PM/YM']*0.1129848333                    # Pitching Moment in N*m
]

invertedCupData = [
    q2v(abs(invertedCup['q'])/0.020885, temp, pressure), # Velocity in m/s
    invertedCup['NF/SF']*4.44822,                        # Normal Force in N
    invertedCup['AF/AF2']*4.44822,                       # Axial Force in N
    invertedCup['PM/YM']*0.1129848333,                   # Pitching Moment in N*m
]

sphereData = [
    q2v(abs(sphere['q'])/0.020885, temp, pressure), # Velocity in m/s
    sphere['NF/SF']*4.44822,                        # Normal Force in N
    sphere['AF/AF2']*4.44822,                       # Axial Force in N
    sphere['PM/YM']*0.1129848333                    # Pitching Moment in N*m
]

# Set up window
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

# Normal Force v Velocity
ax1.set_xlabel('V_inf [m/s]')
ax1.set_ylabel('Normal Forcce [N]')
ax1.plot(
    flatPlateVelData[0],
    flatPlateVelData[1],
    'r-',
    label='Flat Plate',
    zorder=10
)
ax1.plot(
    halfSphereData[0],    
    halfSphereData[1],
    'b-',
    label='Half Sphere',
    zorder=15 
)
ax1.plot(
    invertedCupData[0],
    invertedCupData[1],
    'k-',
    label='Inverted Cup',
    zorder=5
)
ax1.plot(
    sphereData[0],
    sphereData[1],
    'g-',
    label='Sphere',
    zorder=0
)

# Axial Force v Velocity
ax2.set_xlabel('V_inf [m/s]')
ax2.set_ylabel('Axial Force [N]')
ax2.plot(
    flatPlateVelData[0],
    flatPlateVelData[2],
    'r-',
    label='Flat Plate',
    zorder=2
)
ax2.plot(
    halfSphereData[0],
    halfSphereData[2],
    'b-',
    label='Half Sphere',
    zorder=5
)
ax2.plot(
    invertedCupData[0],
    invertedCupData[2],
    'k-',
    label='Inverted Cup',
    zorder=10
)
ax2.plot(
    sphereData[0],
    sphereData[2],
    'g-',
    label='Sphere',
    zorder=0
)

# Normal/Axial Force v Angle of Attack
ax3.set_xlabel('Alpha [deg]')
ax3.set_ylabel('Force [N]')
ax3.plot(
    flatPlateAngData[0],
    flatPlateAngData[1],
    'r-',
    label='Normal Force'
)
ax3.plot(
    flatPlateAngData[0],
    flatPlateAngData[2],
    'b-',
    label='Axial Force'
)

ax1.set_title('Normal Force vs Free Stream Velocity')
ax1.set_xlim(xmin=0)
ax1.legend()
ax2.set_title('Axial Force vs Free Stream Velocity')
ax2.set_xlim(xmin=0)
ax2.legend()
ax3.set_title('Normal/Axial Force vs Angle of Attack')
ax3.set_xlim(xmin=0)
ax3.legend()
plt.show()
