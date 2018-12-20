% List of open inputs
% Smooth: Images to smooth - cfg_files

config = ini2struct('../movrest_config.ini');  % uses function from FileExchange by Andriy Nych
DATA_DIR = config.default.prep_dir;

subjects = {'03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14'; '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

subdir_pattern = fullfile('sub-%s', 'func');
file_pattern = 'sub-%s_task-movierest_run-%02d_space-MNI152NLin2009cAsym_desc-preproc_bold.nii';

nrun = length(subjects); % enter the number of runs here
jobfile = {'/Users/michal/Documents/movrest_2018/spm_batch/smooth_job.m'};  % TODO check if it can be relative :/
jobs = repmat(jobfile, 1, nrun);
inputs = cell(1, nrun);

for crun = 1:nrun
    subdir = sprintf(subdir_pattern, subjects{crun});
    inputs{1, crun} = {
        fullfile(DATA_DIR, subdir, sprintf(file_pattern, subjects{crun}, 1))
        fullfile(DATA_DIR, subdir, sprintf(file_pattern, subjects{crun}, 2))
        }; % Smooth: Images to smooth - cfg_files
end

spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
