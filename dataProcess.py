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

# Set up window
fig1, ax1 = plt.subplots() # Normal Force v Velocity
fig2, ax2 = plt.subplots() # Axial Force v Velocity
fig3, [ax3, ax3_2] = plt.subplots(2) # Normal/Axial Force v Angle of Attack
fig4, [ax4, ax4_2] = plt.subplots(2) # Coefficient of Lift/Drag
fig5, ax5 = plt.subplots() # Pitching Moment v Velocity

# Parameters
wl = 151 # Window Length
po = 2   # Polynomial Order
size = 0.5

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

flatPlateVelXLine, flatPlateVelYLine, a1, b1, c1 = get_AF_line(flatPlateVel.X, flatPlateVel.AF)
halfSphereXLine, halfSphereYLine, a2, b2, c2 = get_AF_line(halfSphere.X, halfSphere.AF)
invertedCupXLine, invertedCupYLine, a3, b3, c3 = get_AF_line(invertedCup.X, invertedCup.AF)
sphereXLine, sphereYLine, a4, b4, c4 = get_AF_line(sphere.X, sphere.AF)

# Axial Force v Velocity
ax2.set_xlabel('V_inf [m/s]')
ax2.set_ylabel('Axial Force [N]')

# Scatter Plot for individual points
ax2.scatter(
    flatPlateVel.X,
    flatPlateVel.AF,
    s=size,
    c='blue'
)
ax2.scatter(
    halfSphere.X,
    halfSphere.AF,
    s=size,
    c='green'
)
ax2.scatter(
    invertedCup.X,
    invertedCup.AF,
    s=size,
    c='red'
)
ax2.scatter(
    sphere.X,
    sphere.AF,
    s=size,
    c='black'
)

# Curve Fit Line
ax2.plot(
    flatPlateVelXLine,
    flatPlateVelYLine,
    'b-',
    label='Flat Plate'
)
ax2.plot(
    halfSphereXLine,
    halfSphereYLine,
    'g-',
    label='Half Sphere'
)
ax2.plot(
    invertedCupXLine,
    invertedCupYLine,
    'r-',
    label='Inverted Cup'
)
ax2.plot(
    sphereXLine,
    sphereYLine,
    'k-',
    label='Sphere'
)

a = [a1, a2, a3, a4]
b = [b1, b2, b3, b4]
c = [c1, c2, c3, c4]

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

flatPlateAngXCL, flatPlateAngYCL, a5, b5, c5, d5 = get_coeff_curve(flatPlateAng.X, flatPlateAng.CL)
flatPlateAngXCD, flatPlateAngYCD, a6, b6, c6, d6 = get_coeff_curve(flatPlateAng.X, flatPlateAng.CD)

ax4.set_xlabel('Alpha [deg]')
ax4.set_ylabel('Lift Coefficient')
ax4_2.set_xlabel('Alpha [deg]')
ax4_2.set_ylabel('Drag Coefficient')
ax4.scatter(
    flatPlateAng.X,
    flatPlateAng.CL,
    s=size,
    c='red'
)
ax4_2.scatter(
    flatPlateAng.X,
    flatPlateAng.CD,
    s=size,
    c='blue'
)
ax4.plot(
    flatPlateAngXCL,
    flatPlateAngYCL,
    'r-',
    label='Coefficient of Lift'
)
ax4_2.plot(
    flatPlateAngXCD,
    flatPlateAngYCD,
    'b-',
    label='Coefficient of Drag'
)

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