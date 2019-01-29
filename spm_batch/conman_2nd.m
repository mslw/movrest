% contrast manager - second level

config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;

model_path = fullfile(WORK_DIR, 'models2', 'flex_factorial_xm1_xm2', ...
    'SPM.mat');

nrun = 1;
jobfile = {'conman_2nd_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(21, nrun);

REST = [0 1/3 1/3 1/3];

for crun = 1:nrun
    % Contrast Manager: Select SPM.mat - cfg_files
    inputs{1, crun} = cellstr(model_path);
    
    % Contrast Manager: Name - cfg_entry
    inputs{2, crun} = 'rest > mov';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{3, crun} = repmat([-1 1/3 1/3 1/3], 1, 5);
    
    % Contrast Manager: Name - cfg_entry
    inputs{4, crun} = 'mov > rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{5, crun} = repmat([1 -1/3 -1/3 -1/3], 1, 5);
    
    % Contrast Manager: Name - cfg_entry
    inputs{6, crun} = 'post fear rest > post neutral rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{7, crun} = [zeros(1,4) REST zeros(1,4) -REST zeros(1,4)];
    
    % Contrast Manager: Name - cfg_entry
    inputs{8, crun} = 'post neutral rest > post fear rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{9, crun} = [zeros(1,4) -REST zeros(1,4) REST zeros(1,4)];
    
    % Contrast Manager: Name - cfg_entry
    inputs{10, crun} = 'post joyful rest > post neutral rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{11, crun} = [zeros(1,4) zeros(1,4) REST -REST zeros(1,4)];
        
    % Contrast Manager: Name - cfg_entry
    inputs{12, crun} = 'post neutral rest > post joyful rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{13, crun} = [zeros(1,4) zeros(1,4) -REST REST zeros(1,4)];
    
    % Contrast Manager: Name - cfg_entry
    inputs{14, crun} = 'post erotic rest > post neutral rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{15, crun} = [REST zeros(1,4) zeros(1,4) -REST zeros(1,4)];
    
    % Contrast Manager: Name - cfg_entry
    inputs{16, crun} = 'post neutral rest > post erotic rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{17, crun} = [-REST zeros(1,4) zeros(1,4) REST zeros(1,4)];
    
    % Contrast Manager: Name - cfg_entry
    inputs{18, crun} = 'post sad rest > post neutral rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{19, crun} = [zeros(1,4) zeros(1,4) zeros(1,4) -REST REST];
    
    % Contrast Manager: Name - cfg_entry
    inputs{20, crun} = 'post neutral rest > post sad rest';
    % Contrast Manager: Weights vector - cfg_entry
    inputs{21, crun} = [zeros(1,4) zeros(1,4) zeros(1,4) REST -REST];
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
