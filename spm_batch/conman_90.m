% second level contrast manager
% for flexible factorial, based on 90 second long movie bins

config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;
dir_2nd_lvl = 'flex_factorial_90';

nrun = 1;
jobfile = {'/Users/michal/Documents/movrest_2018/spm_batch/conman_90_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(19, nrun);
for crun = 1:nrun
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, 'models2', dir_2nd_lvl, 'SPM.mat')); % Contrast Manager: Select SPM.mat - cfg_files
    
    inputs{2, crun} = 'rest > mov'; % Contrast Manager: Name - cfg_entry
    inputs{3, crun} = repmat([-1 1], 1, 5); % Contrast Manager: Weights vector - cfg_entry
    
    inputs{4, crun} = 'mov > rest'; % Contrast Manager: Name - cfg_entry
    inputs{5, crun} = repmat([1 -1], 1, 5); % Contrast Manager: Weights vector - cfg_entry
    
    inputs{6, crun} = 'post fear > post neu'; % Contrast Manager: Name - cfg_entry
    inputs{7, crun} = [0 0 0 1 0 0 0 -1 0 0]; % Contrast Manager: Weights vector - cfg_entry
    
    inputs{8, crun} = 'post neu > post fear'; % Contrast Manager: Name - cfg_entry
    inputs{9, crun} = [0 0 0 -1 0 0 0 1 0 0]; % Contrast Manager: Weights vector - cfg_entry
    
    inputs{10, crun} = 'post neu > post joy'; % Contrast Manager: Name - cfg_entry
    inputs{11, crun} = [0 0 0 0 0 -1 0 1 0 0]; % Contrast Manager: Weights vector - cfg_entry
    
    inputs{12, crun} = 'mov ero > mov neu'; % Contrast Manager: Name - cfg_entry
    inputs{13, crun} = [1 0 0 0 0 0 -1 0 0 0]; % Contrast Manager: Weights vector - cfg_entry
    
    inputs{14, crun} = 'mov fea > mov neu'; % Contrast Manager: Name - cfg_entry
    inputs{15, crun} = [0 0 1 0 0 0 -1 0 0 0]; % Contrast Manager: Weights vector - cfg_entry
    
    inputs{16, crun} = 'plot'; % Contrast Manager: Name - cfg_entry
    inputs{17, crun} = eye(10) - 0.1; % Contrast Manager: Weights matrix - cfg_entry
    
    inputs{18, crun} = 'subject plot'; % Contrast Manager: Name - cfg_entry
    inputs{19, crun} = [zeros(22, 10) eye(22)-1/22]; % Contrast Manager: Weights matrix - cfg_entry
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
