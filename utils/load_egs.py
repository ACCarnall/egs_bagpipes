import numpy as np
import bagpipes as pipes
from astropy.table import Table


def load_egs(ID):
    """ Load egs photometry from v1.0 Stefanon et al. (2017) cat """

    cat = Table.read("../catalogues/hlsp_candels_hst_wfc3_egs-tot-multiband_f160w_v1-1photom_cat.fits").to_pandas()
    cat.index = cat["ID"].astype(str).values

    flux_cols = ['CFHT_u_FLUX', 'ACS_F606W_FLUX', 'ACS_F814W_FLUX',
                 'CFHT_z_FLUX', 'WFC3_F125W_FLUX', 'WFC3_F140W_FLUX',
                 'WFC3_F160W_FLUX', 'IRAC_CH1_FLUX', 'IRAC_CH2_FLUX',
                 'IRAC_CH3_FLUX', 'IRAC_CH4_FLUX']

    err_cols = ['CFHT_u_FLUXERR', 'ACS_F606W_FLUXERR', 'ACS_F814W_FLUXERR',
                'CFHT_z_FLUXERR', 'WFC3_F125W_FLUXERR', 'WFC3_F140W_FLUXERR',
                'WFC3_F160W_FLUXERR', 'IRAC_CH1_FLUXERR', 'IRAC_CH2_FLUXERR',
                'IRAC_CH3_FLUXERR', 'IRAC_CH4_FLUXERR']

    photometry = np.c_[cat.loc[str(ID), flux_cols],
                       cat.loc[str(ID), err_cols]]

    # Limit SNR to 20 sigma in each band
    for i in range(len(photometry)):
        if np.abs(photometry[i, 0]/photometry[i, 1]) > 20.:
            photometry[i, 1] = np.abs(photometry[i, 0]/20.)

    # Limit SNR of IRAC1 and IRAC2 channels to 10 sigma.
    for i in range(1,3):
        if np.abs(photometry[-i, 0]/photometry[-i, 1]) > 10.:
            photometry[-i, 1] = np.abs(photometry[-i, 0]/10.)

    # blow up the errors associated with any N/A points in the photometry
    for i in range(len(photometry)):
        if (photometry[i, 0] == 0.) or (photometry[i, 1] <= 0) or (photometry[i, 0] == -99.):
            photometry[i, 0] = 0.
            photometry[i, 1] = 9.9*10**99.

    return photometry.astype("float")
