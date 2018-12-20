import math
import numpy as np
import pandas


def get_rest_regressors(filename):
    wanted = [
        'csf', 'white_matter', 'global_signal',
        'trans_x', 'trans_y', 'trans_z',
        'rot_x', 'rot_y', 'rot_z',
        'a_comp_cor_00', 'a_comp_cor_01', 'a_comp_cor_02',
        'a_comp_cor_03', 'a_comp_cor_04', 'a_comp_cor_05',
        'framewise_displacement',
        ]
    # TODO: add constant & linear trend
    t = pandas.read_table(filename)
    regressors = t.loc[:, wanted]
    regressors.fillna(value=0, inplace=True)

    regressors['constant'] = np.ones(regressors.shape[0])
    regressors['linear_trend'] = np.arange(regressors.shape[0], dtype=np.float)

    return regressors.values


def time_to_volume(time, tr):
    return math.ceil(time / tr)
