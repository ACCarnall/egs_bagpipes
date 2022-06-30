import numpy as np
import bagpipes as pipes
import sys

from astropy.table import Table

sys.path.append("../utils")
from load_egs import load_egs


def get_fit_instructions():
    """ Set up the desired fit_instructions dictionary. """

    dust = {}
    dust["type"] = "Calzetti"
    dust["eta"] = 2.
    dust["Av"] = (0., 4.)

    zmet_factor = (0.02/0.014)

    nebular = {}
    nebular["logU"] = -3.
    #nebular["metallicity"] = (0.1/zmet_factor, 3.5/zmet_factor)
    #nebular["metallicity_prior"] = "log_10"

    dblplaw = {}
    dblplaw["massformed"] = (0., 13.)
    dblplaw["metallicity"] = (0.1/zmet_factor, 3.5/zmet_factor)
    dblplaw["metallicity_prior"] = "log_10"
    dblplaw["alpha"] = (0.1, 1000.)
    dblplaw["alpha_prior"] = "log_10"
    dblplaw["beta"] = (0.1, 1000.)
    dblplaw["beta_prior"] = "log_10"
    dblplaw["tau"] = (0.1, 15.)

    fit_instructions = {}
    fit_instructions["dust"] = dust
    fit_instructions["dblplaw"] = dblplaw
    fit_instructions["nebular"] = nebular
    fit_instructions["t_bc"] = 0.01
    fit_instructions["redshift"] = (0., 10.)

    return fit_instructions


filt_list = np.loadtxt("../filters/filt_list.txt", dtype="str")

# Load list of objects to be fitted from catalogue.
cat = Table.read("../catalogues/hlsp_candels_hst_wfc3_egs-tot-multiband_f160w_v1-1photom_cat.fits").to_pandas()
cat.index = cat["ID"].astype(str).values
cat = cat.groupby(cat["FLAGS"] == 0).get_group(True)
print(cat.shape)

IDs = cat.index

fit_instructions = get_fit_instructions()

fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_egs, run="egs_v1",
                              cat_filt_list=filt_list, vary_filt_list=False,
                              make_plots=False, time_calls=False,
                              spectrum_exists=False, full_catalogue=True)

fit_cat.fit(n_live=1000, verbose=False, mpi_serial=True)
