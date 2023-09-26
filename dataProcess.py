import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import savgol_filter as sf
from dataFunctions import *

# ------------------------------------------------------------------------------
# ---------------------------------Main Program---------------------------------
# ------------------------------------------------------------------------------

# Read Files
path = str(Path(__file__).parent)+'/Data' # Finds current path and Data folder
files = [
    path+'/Zero Velocity Flat Plate Angle.csv',
    path+'/Flat Plate Angle.csv',
    path+'/Flat Plate Velocity.csv',
    path+'/Half Sphere.csv',
    path+'/Inverted Cup.csv',
    path+'/Sphere.csv'
]

data = read_files(files)

zeroVel, flatPlateAng, flatPlateVel, halfSphere, invertedCup, sphere = data_split(data)

flatPlateVelXLine, flatPlateVelYLine, a1, b1, c1 = get_xy_line(flatPlateVel.X, flatPlateVel.AF)
halfSphereXLine, halfSphereYLine, a2, b2, c2 = get_xy_line(halfSphere.X, halfSphere.AF)
invertedCupXLine, invertedCupYLine, a3, b3, c3 = get_xy_line(invertedCup.X, invertedCup.AF)
sphereXLine, sphereYLine, a4, b4, c4 = get_xy_line(sphere.X, sphere.AF)

# Set up window
fig1, ax1 = plt.subplots() # Normal Force v Velocity

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

fig2, ax2 = plt.subplots() # Axial Force v Velocity
# Axial Force v Velocity
ax2.set_xlabel('V_inf [m/s]')
ax2.set_ylabel('Axial Force [N]')
size = 0.5

# Scatter Plot for individual points
plt.scatter(
    flatPlateVel.X,
    flatPlateVel.AF,
    s=size,
    c='blue'
)
plt.scatter(
    halfSphere.X,
    halfSphere.AF,
    s=size,
    c='green'
)
plt.scatter(
    invertedCup.X,
    invertedCup.AF,
    s=size,
    c='red'
)
plt.scatter(
    sphere.X,
    sphere.AF,
    s=size,
    c='black'
)

# Curve Fit Line
plt.plot(
    flatPlateVelXLine,
    flatPlateVelYLine,
    'b-',
    label='Flat Plate'
)
plt.plot(
    halfSphereXLine,
    halfSphereYLine,
    'g-',
    label='Half Sphere'
)
plt.plot(
    invertedCupXLine,
    invertedCupYLine,
    'r-',
    label='Inverted Cup'
)
plt.plot(
    sphereXLine,
    sphereYLine,
    'k-',
    label='Sphere'
)

a = [a1, a2, a3, a4]
b = [b1, b2, b3, b4]
c = [c1, c2, c3, c4]

fig3, [ax3, ax3_2] = plt.subplots(2) # Normal/Axial Force v Angle of Attack
# Normal/Axial Force v Angle of Attack
ax3.set_xlabel('Alpha [deg]')
ax3.set_ylabel('Normal Force [N]')
ax3.plot(
    flatPlateAng.X,
    flatPlateAng.NF,
    'r-',
    label='Normal Force'
)
ax3_2.set_xlabel('Alpha [deg]')
ax3_2.set_ylabel('Axial Force [N]')
ax3_2.plot(
    flatPlateAng.X,
    flatPlateAng.AF,
    'b-',
    label='Axial Force'
)

fig4, [ax4, ax4_2] = plt.subplots(2) # Coefficient of Lift/Drag
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

fig5, ax5 = plt.subplots() # Pitching Moment v Velocity
# Pitching Moment v Wind Velocity
ax5.set_xlabel('V_inf [m/s]')
ax5.set_ylabel('Pitching Moment [N*m]')
ax5.plot(
    flatPlateVel.X,
    flatPlateVel.PM,
    'r-',
    label='Flat Plate',
    zorder=10
)
ax5.plot(
    halfSphere.X,
    halfSphere.PM,
    'b-',
    label='Half Sphere',
    zorder=15
)
ax5.plot(
    invertedCup.X,
    invertedCup.PM,
    'k-',
    label='Inverted Cup',
    zorder=5
)
ax5.plot(
    sphere.X,
    sphere.PM,
    'g-',
    label='Sphere',
    zorder=0
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
ax5.set_title('Pitching Moment vs Free Stream Velocity')
ax5.set_xlim(xmin=0)
ax5.legend()
print("Curve Fit Lines:")
for i in range(0, len(a)):
    print("y%s = %.5f*x^2 + %.5f*x + %.5f" % (i+1, a[i], b[i], c[i]))
ax2.set_title('Axial Force vs Free Stream Velocity')
plt.show()