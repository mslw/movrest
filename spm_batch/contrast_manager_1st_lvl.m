config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;

subjects = {'03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12';...
            '14'; '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25';...
            '26'; '27'};

nrun = length(subjects);
jobfile = {'contrast_manager_1st_lvl_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(1, nrun);
for crun = 1:nrun
    % Contrast Manager: Select SPM.mat - cfg_files
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, 'models', sprintf('sub-%s', subjects{crun}), 'SPM.mat'));
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
