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

[zeroVel, flatPlateAng, flatPlateVel, halfSphere, invertedCup, sphere], lift, drag = data_split(data)

# Set up window
fig1, ax1 = plt.subplots() # Normal Force v Velocity
fig2, ax2 = plt.subplots() # Axial Force v Velocity
fig3, [ax3, ax3_2, ax3_3] = plt.subplots(3) # Normal/Axial Force v Angle of Attack for Flat Plate
fig4, [ax4, ax4_2, ax4_3] = plt.subplots(3) # Coefficient of Lift/Drag for Flat Plate
fig5, ax5 = plt.subplots() # Pitching Moment v Velocity
fig6, ax6 = plt.subplots() # Coefficient of Lift v Velocity
fig7, ax7 = plt.subplots() # Coefficient of Drag v Velocity
fig8, ax8 = plt.subplots() # Coefficient of Pitching Moment v Velocity
fig9, [ax9, ax9_2] = plt.subplots(2) # Lift/Drag v Angle of Attack

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
    s=size
)
ax1.scatter(
    halfSphere.X,
    halfSphere.NF,
    c='green',
    s=size    
)
ax1.scatter(
    invertedCup.X,
    invertedCup.NF,
    s=size,
    c='red'
)
ax1.scatter(
    sphere.X,
    sphere.NF,
    s=size,
    c='black'
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

flatPlateAngXNF, flatPlateAngYNF, a1, b1 = get_linear_curve(flatPlateAng.X, flatPlateAng.NF)
flatPlateAngXAF, flatPlateAngYAF, a2, b2 = get_linear_curve(flatPlateAng.X, flatPlateAng.AF)
flatPlateAngXPM, flatPlateAngYPM, a3, b3 = get_linear_curve(flatPlateAng.X, flatPlateAng.PM)
zeroVelXNF, zeroVelYNF, a4, b4 = get_linear_curve(zeroVel.X, zeroVel.NF)
zeroVelXAF, zeroVelYAF, a5, b5 = get_linear_curve(zeroVel.X, zeroVel.AF)
zeroVelXPM, zeroVelYPM, a6, b6 = get_linear_curve(zeroVel.X, zeroVel.PM)

flatPlateAngXNF, flatPlateAngYNF = calibrate_curve(flatPlateAng.X, a1, a4, b1, b4)
flatPlateAngXAF, flatPlateAngYAF = calibrate_curve(flatPlateAng.X, a2, a5, b2, b5)
flatPlateAndXPM, flatPlateAngYPM = calibrate_curve(flatPlateAng.X, a3, a6, b3, b6)

# Normal/Axial Force v Angle of Attack
ax3.set_xlabel('Alpha [deg]')
ax3.set_ylabel('Normal Force [N]')
ax3_2.set_xlabel('Alpha [deg]')
ax3_2.set_ylabel('Axial Force [N]]')
ax3_3.set_xlabel('Alpha [deg]')
ax3_3.set_ylabel('Pitching Moment [N*m]')
ax3.scatter(
    flatPlateAng.X,
    flatPlateAng.NF,
    s=size,
    c='red'
)
ax3.scatter(
    zeroVel.X,
    zeroVel.NF,
    s=size,
    c='black'
)
ax3_2.scatter(
    flatPlateAng.X,
    flatPlateAng.AF,
    s=size,
    c='blue'
)
ax3_2.scatter(
    zeroVel.X,
    zeroVel.AF,
    s=size,
    c='black'
)
ax3_3.scatter(
    flatPlateAng.X,
    flatPlateAng.PM,
    s=size,
    c='green'
)
ax3_3.scatter(
    zeroVel.X,
    zeroVel.PM,
    s=size,
    c='black'
)

# Curve Fit Lines (Linear)
ax3.plot(
    flatPlateAngXNF,
    flatPlateAngYNF,
    'r-',
    label='Calibrated Normal Force',
    linewidth=lnwidth
)
ax3.plot(
    zeroVelXNF,
    zeroVelYNF,
    'k-',
    label='Zero Velocity',
    linewidth=lnwidth
)
ax3_2.plot(
    flatPlateAngXAF,
    flatPlateAngYAF,
    'b-',
    label='Calibrated Axial Force',
    linewidth=lnwidth
)
ax3_2.plot(
    zeroVelXAF,
    zeroVelYAF,
    'k-',
    label='Zero Velocity',
    linewidth=lnwidth
)
ax3_3.plot(
    flatPlateAngXPM,
    flatPlateAngYPM,
    'g-',
    label='Calibrated Pitching Moment',
    linewidth=lnwidth
)
ax3_3.plot(
    zeroVelXPM,
    zeroVelYPM,
    'k-',
    label='Zero Velocity',
    linewidth=lnwidth
)

flatPlateAngXCL, flatPlateAngYCL, _, _= get_linear_curve(flatPlateAng.X, flatPlateAng.CL)
flatPlateAngXCD, flatPlateAngYCD, _, _ = get_linear_curve(flatPlateAng.X, flatPlateAng.CD)
flatPlateAngXCM, flatPlateAngYCM, _, _ = get_linear_curve(flatPlateAng.X, flatPlateAng.CM)

ax4.set_xlabel('Alpha [deg]')
ax4.set_ylabel('Lift Coefficient')
ax4_2.set_xlabel('Alpha [deg]')
ax4_2.set_ylabel('Drag Coefficient')
ax4_3.set_xlabel('Alpha [deg]')
ax4_3.set_ylabel('Pitching Moment Coefficient')
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
ax4_3.scatter(
    flatPlateAng.X,
    flatPlateAng.CM,
    s=size,
    c='green'
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
ax4_3.plot(
    flatPlateAngXCM,
    flatPlateAngYCM,
    'g-',
    label='Coefficient of Pitching Moment',
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

# Coefficient of Lift v Velocity
ax6.set_xlabel('V_inf [m/s]')
ax6.set_ylabel('Coefficient of Lift')
ax6.scatter(
    flatPlateVel.X,
    flatPlateVel.CL,
    c='blue',
    s=size,
    label='Flat Plate'
)
ax6.scatter(
    halfSphere.X,
    halfSphere.CL,
    c='green',
    s=size,
    label='Half Sphere'
)
ax6.scatter(
    invertedCup.X,
    invertedCup.CL,
    c='red',
    s=size,
    label='Inverted Cup'
)
ax6.scatter(
    sphere.X,
    sphere.CL,
    c='black',
    s=size,
    label='Sphere'
)

# Coefficient of Drag v Velocity
ax7.set_xlabel('V_inf [m/s]')
ax7.set_ylabel('Coefficient of Drag')
ax7.scatter(
    flatPlateVel.X,
    flatPlateVel.CD,
    c='blue',
    s=size,
    label='Flat Plate'
)
ax7.scatter(
    halfSphere.X,
    halfSphere.CD,
    c='green',
    s=size,
    label='Half Sphere'
)
ax7.scatter(
    invertedCup.X,
    invertedCup.CD,
    c='red',
    s=size,
    label='Inverted Cup'
)
ax7.scatter(
    sphere.X,
    sphere.CD,
    c='black',
    s=size,
    label='Sphere'
)

# Coefficient of Pitching Moment
ax8.set_xlabel('V_inf [m/s]')
ax8.set_ylabel('Coefficient of Pitching Moment')
ax8.scatter(
    flatPlateVel.X,
    flatPlateVel.CM,
    c='blue',
    s=size,
    label='Flat Plate'
)
ax8.scatter(
    halfSphere.X,
    halfSphere.CM,
    c='green',
    s=size,
    label='Half Sphere'
)
ax8.scatter(
    invertedCup.X,
    invertedCup.CM,
    c='red',
    s=size,
    label='Inverted Cup'
)
ax8.scatter(
    sphere.X,
    sphere.CM,
    c='black',
    s=size,
    label='Sphere'
)

flatPlateAngXLF, flatPlateAngYLF, _, _ = get_linear_curve(flatPlateAng.X, lift)
flatPlateAngXDF, flatPlateAngYDF, _, _ = get_linear_curve(flatPlateAng.X, drag)

# Lift/Drag Forces v Angle of Attack
ax9.set_xlabel('Alpha [deg]')
ax9.set_ylabel('Lift Force [N]')
ax9_2.set_xlabel('Alpha [deg]')
ax9_2.set_ylabel('Drag Force [N]')
ax9.scatter(
    flatPlateAng.X,
    lift,
    s=size,
    c='red'
)
ax9_2.scatter(
    flatPlateAng.X,
    drag,
    s=size,
    c='blue'
)
ax9.plot(
    flatPlateAngXLF,
    flatPlateAngYLF,
    'r-',
    label='Lift Force',
    linewidth=lnwidth
)
ax9_2.plot(
    flatPlateAngXDF,
    flatPlateAngYDF,
    'b-',
    label='Drag Force',
    linewidth=lnwidth
)

# Graph formating
ax1.set_title('Normal Force vs Free Stream Velocity')
ax1.set_xlim(xmin=0)
ax1.legend()
ax1.grid()
ax2.set_title('Axial Force vs Free Stream Velocity')
ax2.set_xlim(xmin=0)
ax2.legend()
ax2.grid()
ax3.set_title('Force/Moment vs Angle of Attack')
ax3.set_xlim(xmin=0)
ax3.grid()
ax3.legend()
ax3_2.set_xlim(xmin=0)
ax3_2.grid()
ax3_2.legend()
ax3_3.set_xlim(xmin=0)
ax3_3.grid()
ax3_3.legend()
ax4.set_title('Coefficients vs Angle of Attack')
ax4.set_xlim(xmin=0)
ax4.grid()
ax4_2.set_xlim(xmin=0)
ax4_2.grid()
ax4_3.set_xlim(xmin=0)
ax4_3.grid()
ax5.set_title('Pitching Moment vs Free Stream Velocity')
ax5.set_xlim(xmin=0)
ax5.grid()
ax5.legend()
ax6.set_title('Coefficient of Lift vs Free Stream Velocity')
ax6.set_xlim(xmin=0)
ax6.set_ylim(ymin=-0.3, ymax=0.3)
ax6.legend()
ax6.grid()
ax7.set_title('Coefficient of Drag vs Free Stream Velocity')
ax7.set_xlim(xmin=0)
ax7.set_ylim(ymin=-0.02, ymax=0.3)
ax7.legend()
ax7.grid()
ax8.set_title('Coefficient of Pitching Moment vs Free Stream Velocity')
ax8.set_xlim(xmin=0)
ax8.set_ylim(ymin=-200, ymax=200)
ax8.legend()
ax8.grid()
ax9.set_title('Lift/Drag Forces vs Angle of Attack')
ax9.set_xlim(xmin=0)
ax9.grid()
ax9_2.set_xlim(xmin=0)
ax9_2.grid()
plt.show()