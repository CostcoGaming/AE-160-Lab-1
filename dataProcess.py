import pandas as pd
import matplotlib.pyplot as plt

def read_files(files):
    new_files = [0]*len(files)
    for i in range(0,len(files)):
        new_files[i] = pd.read_csv(files[i], skiprows=[1])

    return new_files

path = r"D:\School\'23 Fall\Lab\AE 160\Lab 1"
files = [
    path+'\Flat Plate Angle.csv',
    path+'\Flat Plate Velocity.csv',
    path+'\Half Sphere.csv',
    path+'\Inverted Cup.csv',
    path+'\Sphere.csv'
]

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
    flatPlateVel['V_ref']/2.237,         # Velocity in m/s
    flatPlateVel['NF/SF']*4.44822,       # Normal Force in N
    flatPlateVel['AF/AF2']*4.44822,      # Axial Force in N
    flatPlateVel['PM/YM']*0.1129848333,  # Pitching Moment in N*m
]

halfSphereData = [
    halfSphere['V_ref']/2.237,           # Velocity in m/s
    halfSphere['NF/SF']*4.44822,         # Normal Force in N
    halfSphere['AF/AF2']*4.44822,        # Axial Force in N
    halfSphere['PM/YM']*0.1129848333     # Pitching Moment in N*m
]

sphereData = [
    sphere['V_ref']/2.237,               # Velocity in m/s
    sphere['NF/SF']*4.44822,             # Normal Force in N
    sphere['AF/AF2']*4.44822,            # Axial Force in N
    sphere['PM/YM']*0.1129848333         # Pitching Moment in N*m
]

# Set up window
fig, ax = plt.subplots()

# Axial Force
ax.set_xlabel('V_inf [m/s]')
ax.set_ylabel('Axial Force [N]')
ax.plot(
    flatPlateVelData[0],
    flatPlateVelData[2],
    'r-',
    label='Flat Plate'
)
ax.plot(
    halfSphereData[0],
    halfSphereData[2],
    'b-',
    label='Half Sphere'
)
ax.plot(
    sphereData[0],
    sphereData[2],
    'g-',
    label='Sphere'
)

plt.suptitle('Axial Force vs Free Stream Velocity')
plt.legend()
plt.show()