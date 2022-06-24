"""
#-----------------------------------------------------------------------------
@email: akhanna2@ucmerced.edu || quantphobia@gmail.com 
@lab: Dr. Isborn
@place: UC Merced
@date: May.31.2022
@author: Ajay Khanna |Git: Ajaykhanna|Twitter: @samdig| LinkedIn: ajay-khanna
"""
#-----------------------------------------------------------------------------

# Importing the necessary libraries for the program to run.
import re
import argparse
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt

# Printing the title of the program and the author's name.
print("#-------| Python Program to Parse Gaussian Optimization Log Files |-------#")
print("#-------| Written by AjayKhanna(@samdig) | -------#")
print("#-------| Running | -------#")

# Parsing the command line arguments.
parser = argparse.ArgumentParser(description='Python Program to Parse Gaussian16 Geometry Optimization Log File And Plot Progress of The Optimization Process')
parser.add_argument('--input', '-i', type=argparse.FileType('r'), required=True, help="Input Gaussian Optimization Log File",) 
parser.add_argument('--output', '-o', type=argparse.FileType('w'), required=True, help='Output Filename for Image')
args = parser.parse_args()

def pattern_search(pattern,filename):
    """
    It takes a pattern and a file as input and returns a list of values that match the pattern
    
    :param pattern: the string you want to search for
    :param filename: the name of the file you want to search through
    :return: A list of floats
    """
    dummy = []
    if pattern == "Predicted change in Energy=":
        for line in filename:
            for match in re.finditer(pattern, line):
                dummy.append(line.split()[3].split("=")[1].replace("D", "E"))
    elif pattern == "SCF Done:":
        for line in filename:
            for match in re.finditer(pattern, line):
                #print(line.split()[4])
                dummy.append(line.split()[4])
    else:
        for line in filename:
            for match in re.finditer(pattern, line):
                dummy.append(float(line.split()[2]))
    return dummy

# Creating a list of strings and then calling the function pattern_search() to search for the strings
# in the file.
search_patterns = ["SCF Done:",
                   "Predicted change in Energy=",
                   "Maximum Force", 
                   "RMS     Force",
                   "Maximum Displacement",
                   "RMS     Displacement"]

# Searching for the pattern in the file and returning a list of values that match the pattern.
scf_energy = np.array(pattern_search(search_patterns[0], open(args.input.name)))
delta_e    = np.array(pattern_search(search_patterns[1], open(args.input.name)))
delta_e    = np.array([item.replace(" ",",") for item in delta_e])
max_force  = np.array(pattern_search(search_patterns[1], open(args.input.name)))
rms_force  = np.array(pattern_search(search_patterns[2], open(args.input.name)))
max_displ  = np.array(pattern_search(search_patterns[3], open(args.input.name)))
rms_displ  = np.array(pattern_search(search_patterns[4], open(args.input.name)))

# Creating a 2x3 grid of plots.
#formatter = ticker.ScalarFormatter(useMathText=True)
#formatter.set_scientific(True) 
#formatter.set_powerlimits((1,1))

fig, axs = plt.subplots(2, 3, figsize=(12, 5))
#axs[0][1].set_visible(False)

axs[0, 0].plot(np.arange(1, len(scf_energy)+1), scf_energy, 'tab:red',)
axs[0, 0].set_title('SCF Energy (AU)') # Ploting the SCF Energy

axs[0, 1].plot(np.arange(1, len(scf_energy)+1), delta_e, 'tab:grey',)
axs[0, 1].set_title('Delta-E') # Ploting the Delta-E

axs[0, 2].plot(np.arange(1, len(scf_energy)+1), max_force, 'tab:orange')
axs[0, 2].set_title('Max. Force') # Ploting the Max. Force

axs[1, 0].plot(np.arange(1, len(scf_energy)+1), max_displ, 'tab:green')
axs[1, 0].set_title('Max. Displacement') # Ploting the Max. Displacement

axs[1, 1].plot(np.arange(1, len(scf_energy)+1), rms_force, 'tab:blue')
axs[1, 1].set_title('RMS Force') # Ploting the RMS Force

axs[1, 2].plot(np.arange(1, len(scf_energy)+1), rms_displ, 'tab:pink')
axs[1, 2].set_title('RMS Displacement') # Ploting the RMS Displacement

# Setting the x and y labels for each of the subplots.
for ax in axs.flat:
    ax.set_xlabel('#Cycles',fontsize = 10)
    ax.set_ylabel('Progress', fontsize = 10)
    #ax.set_xticks(np.arange(1, len(rms_force)//2))
    #ax.set_yscale('log')
    ax.grid(visible=True, axis='both', linestyle='-.')
    #ax.label_outer()
    #ax.yaxis.set_major_formatter(formatter)

# Saving the plot as an image file.
fig.tight_layout()
plt.savefig(str(args.output.name), dpi=150)
print("#-------| Done | -------#")