from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.lines as mlines
from plot_tune import *

def cpymad_set_isis_cycle_time(madx_instance, max_E, time):
    # Ensure time is a float and in valid increments
    if not isinstance(time, float) or time < 0.0 or time > 10.0 or (time * 10) % 5 != 0:
        print(f"Error: time must be a float between 0.0 and 10.0 in 0.5 increments. Received: {time}")
        return

    # Generate dataframe of synchrotron energy and related info
    energy_df = synchrotron_energy_df(max_E, intervals=20)

    # store some values for this time point
    try:
        energy = energy_df[energy_df['Time [ms]'] == time]['Energy [MeV]'].iloc[0]
        pc = energy_df[energy_df['Time [ms]'] == time]['Momentum [GeV/c]'].iloc[0]
    except IndexError:
        print(f"Error: No matching time value found in energy dataframe for time = {time} ms")
        return

    # set the beam to this energy in cpymad
    madx_instance.input(f'beam, particle = proton, pc = {pc};')

    # print confirmation
    print(f'ISIS cpymad run, energy set to {energy} MeV, pc = {pc}')



cpymad_logfile = 'cpymad_logfile.txt'
sequence_name = 'synchrotron'

madx = cpymad_start(cpymad_logfile)

lattice_folder = 'ISIS_Synchotron_Model\\Lattice_Files\\04_New_Harmonics\\'

madx.call(file=lattice_folder+'ISIS.injected_beam')
madx.call(file=lattice_folder+'ISIS.strength')
madx.call(file=lattice_folder+'2023.strength')
madx.call(file=lattice_folder+'ISIS.elements')
madx.call(file=lattice_folder+'ISIS.sequence')

cpymad_check_and_use_sequence(madx, cpymad_logfile, sequence_name)

max_E = 800 # 800 MeV

time_input = float(input("Start: "))
#time_array = np.linspace(float(time_input), float(time_input), 0.5)


cpymad_set_isis_cycle_time(madx, max_E, time_input)

energy_df = synchrotron_energy_df(max_E, intervals=20)



cpymad_plot_madx_twiss_quads(madx, twiss_0, title='Initial lattice tune')  

set_tune_DW(madx, cpymad_logfile, 4.331, 3.731, 0.0)

twiss_1 = cpymad_madx_twiss(madx, cpymad_logfile, sequence_name)

cpymad_plot_madx_twiss_quads(madx, twiss_1, title='Set tune using DW method') 