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
lnwidth = 2

flatPlateVelXNF, flatPlateVelYNF, _, _ = get_linear_curve(flatPlateVel.X, flatPlateVel.NF)
halfSphereXNF, halfSphereYNF, _, _ = get_linear_curve(halfSphere.X, halfSphere.NF)
invertedCupXNF, invertedCupYNF, _, _ = get_linear_curve(invertedCup.X, invertedCup.NF)
sphereXNF, sphereYNF, _, _ = get_linear_curve(sphere.X, sphere.NF)

# Normal Force v Velocity
ax1.set_xlabel('V_inf [m/s]')
ax1.set_ylabel('Normal Force [N]')
ax1.scatter(
    flatPlateVel.X,
    flatPlateVel.NF,
    c='blue',
    s=size,
)
ax1.scatter(
    halfSphere.X,
    halfSphere.NF,
    c='green',
    s=size,    
)
ax1.scatter(
    invertedCup.X,
    invertedCup.NF,
    s=size,
    c='red',
)
ax1.scatter(
    sphere.X,
    sphere.NF,
    s=size,
    c='black',
)

# Curve Fit Lines (Linear)
ax1.plot(
    flatPlateVelXNF,
    flatPlateVelYNF,
    'b-',
    label='Flat Plate',
    linewidth=lnwidth
)
ax1.plot(
    halfSphereXNF,
    halfSphereYNF,
    'g-',
    label='Half Sphere',
    linewidth=lnwidth
)
ax1.plot(
    invertedCupXNF,
    invertedCupYNF,
    'r-',
    label='Inverted Cup',
    linewidth=lnwidth
)
ax1.plot(
    sphereXNF,
    sphereYNF,
    'k-',
    label='Sphere',
    linewidth=lnwidth
)

flatPlateVelXAF, flatPlateVelYAF, _, _, _ = get_quadratic_curve(flatPlateVel.X, flatPlateVel.AF)
halfSphereXAF, halfSphereYAF, _, _, _ = get_quadratic_curve(halfSphere.X, halfSphere.AF)
invertedCupXAF, invertedCupYAF, _, _, _ = get_quadratic_curve(invertedCup.X, invertedCup.AF)
sphereXAF, sphereYAF, _, _, _ = get_quadratic_curve(sphere.X, sphere.AF)

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

# Curve Fit Lines (Quadratic)
ax2.plot(
    flatPlateVelXAF,
    flatPlateVelYAF,
    'b-',
    label='Flat Plate',
    linewidth=lnwidth
)
ax2.plot(
    halfSphereXAF,
    halfSphereYAF,
    'g-',
    label='Half Sphere',
    linewidth=lnwidth
)
ax2.plot(
    invertedCupXAF,
    invertedCupYAF,
    'r-',
    label='Inverted Cup',
    linewidth=lnwidth
)
ax2.plot(
    sphereXAF,
    sphereYAF,
    'k-',
    label='Sphere',
    linewidth=lnwidth
)

flatPlateAngXNF, flatPlateAngYNF, _, _ = get_linear_curve(flatPlateAng.X, flatPlateAng.NF)
flatPlateAngXAF, flatPlateAngYAF, _, _ = get_linear_curve(flatPlateAng.X, flatPlateAng.AF)

# Normal/Axial Force v Angle of Attack
ax3.set_xlabel('Alpha [deg]')
ax3.set_ylabel('Normal Force [N]')
ax3_2.set_xlabel('Alpha [deg]')
ax3_2.set_ylabel('Axial Force [N]]')
ax3.scatter(
    flatPlateAng.X,
    flatPlateAng.NF,
    s=size,
    c='red'
)
ax3_2.scatter(
    flatPlateAng.X,
    flatPlateAng.AF,
    s=size,
    c='blue'
)

# Curve Fit Lines (Linear)
ax3.plot(
    flatPlateAngXNF,
    flatPlateAngYNF,
    'r-',
    label='Normal Force',
    linewidth=lnwidth
)
ax3_2.plot(
    flatPlateAngXAF,
    flatPlateAngYAF,
    'b-',
    label='Axial Force',
    linewidth=lnwidth
)

flatPlateAngXCL, flatPlateAngYCL, _, _, _, _ = get_cubic_curve(flatPlateAng.X, flatPlateAng.CL)
flatPlateAngXCD, flatPlateAngYCD, _, _, _, _ = get_cubic_curve(flatPlateAng.X, flatPlateAng.CD)

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

# Curve Fit Lines (Cubic)
ax4.plot(
    flatPlateAngXCL,
    flatPlateAngYCL,
    'r-',
    label='Coefficient of Lift',
    linewidth=lnwidth
)
ax4_2.plot(
    flatPlateAngXCD,
    flatPlateAngYCD,
    'b-',
    label='Coefficient of Drag',
    linewidth=lnwidth
)

flatPlateVelXPM, flatPlateVelYPM, _, _ = get_linear_curve(flatPlateVel.X, flatPlateVel.PM)
halfSphereXPM, halfSphereYPM, _, _ = get_linear_curve(halfSphere.X, halfSphere.PM)
invertedCupXPM, invertedCupYPM, _, _ = get_linear_curve(invertedCup.X, invertedCup.PM)
sphereXPM, sphereYPM, _, _ = get_linear_curve(sphere.X, sphere.PM)

# Pitching Moment v Wind Velocity
ax5.set_xlabel('V_inf [m/s]')
ax5.set_ylabel('Pitching Moment [N*m]')
ax5.scatter(
    flatPlateVel.X,
    flatPlateVel.PM,
    s=size,
    c='blue'
)
ax5.scatter(
    halfSphere.X,
    halfSphere.PM,
    s=size,
    c='green'
)
ax5.scatter(
    invertedCup.X,
    invertedCup.PM,
    s=size,
    c='red'
)
ax5.scatter(
    sphere.X,
    sphere.PM,
    s=size,
    c='black'
)

# Curve Fit Lines (Linear)
ax5.plot(
    flatPlateVelXPM,
    flatPlateVelYPM,
    'b-',
    label='Flat Plate',
    linewidth=lnwidth
)
ax5.plot(
    halfSphereXPM,
    halfSphereYPM,
    'g-',
    label='Half Sphere',
    linewidth=lnwidth
)
ax5.plot(
    invertedCupXPM,
    invertedCupYPM,
    'r-',
    label='Inverted Cup',
    linewidth=lnwidth
)
ax5.plot(
    sphereXPM,
    sphereYPM,
    'k-',
    label='Sphere',
    linewidth=lnwidth
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
plt.show()