import configparser
import os
from nilearn import plotting

config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

spm_dir = os.path.join(WORK_DIR, 'models2', 'flex_factorial_xm1_xm2')
fig_dir_voxel = os.path.join(WORK_DIR, 'figures', 'fwe')
fig_dir_clust = os.path.join(WORK_DIR, 'figures', 'fwec')

if not os.path.exists(fig_dir_voxel):
    os.makedirs(fig_dir_voxel)

if not os.path.exists(fig_dir_clust):
    os.makedirs(fig_dir_clust)

contrasts = {
    1: 'rest > mov',
    2: 'mov > rest',
    3: 'post fear rest > post neutral rest',
    4: 'post neutral rest > post fear rest',
    5: 'post joyful rest > post neutral rest',
    6: 'post neutral rest > post joyful rest',
    7: 'post erotic rest > post neutral rest',
    8: 'post neutral rest > post erotic rest',
    9: 'post sad rest > post neutral rest',
    10: 'post neutral rest > post sad rest',
}

for cn in contrasts:
    stat_map = os.path.join(spm_dir, 'spmT_{:04d}_contrastFWE.nii'.format(cn))
    fig_path = os.path.join(fig_dir_voxel,
                            'contrast_{:02d}_FWE.png'.format(cn))
    plotting.plot_glass_brain(stat_map, threshold=None, colorbar=True,
                              title=contrasts[cn], output_file=fig_path)

    if cn in (1, 2):
        continue  # we kept the first two FWE
    stat_map = os.path.join(spm_dir, 'spmT_{:04d}_contrastFWEc.nii'.format(cn))
    fig_path = os.path.join(fig_dir_clust,
                            'contrast_{:02d}_FWEc.png'.format(cn))
    plotting.plot_glass_brain(stat_map, threshold=None, colorbar=True,
                              title=contrasts[cn], output_file=fig_path)
