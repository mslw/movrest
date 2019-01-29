% List of open inputs
% Results Report: Select SPM.mat - cfg_files

config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;

model_path = fullfile(WORK_DIR, 'models2', 'flex_factorial_xm1_xm2', ...
    'SPM.mat');

nrun = 1; % enter the number of runs here
jobfile = {'results_report_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(1, nrun);
for crun = 1:nrun
    % Results Report: Select SPM.mat - cfg_files
    inputs{1, crun} = cellstr(model_path);
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
