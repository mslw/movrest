config = ini2struct('../movrest_config.ini');  % uses function from FileExchange by Andriy Nych
DATA_DIR = config.default.prep_dir;
WORK_DIR = config.default.work_dir;

subjects = {'03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14'; '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

% smoothed data pattern
subdir_pattern = fullfile('sub-%s', 'func');
file_pattern = 'ssub-%s_task-movierest_run-%02d_space-MNI152NLin2009cAsym_desc-preproc_bold.nii';
mask_pattern = 'sub-%s_task-movierest_run-01_space-MNI152NLin2009cAsym_desc-brain_mask.nii';  % 1st run

% conditions & regressors filename patterns, subject_code & run to be filled
conditions_pattern = 'sub-%s_task-movierest_run-%02d_events.mat';
regressors_pattern = 'sub-%s_task-movierest_run-%02d_regressors.mat';

nrun = length(subjects);

jobfile = {'first_level_explicit_mask_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(8, nrun);
for crun = 1:nrun
    
    subject = subjects{crun};
    
    % fMRI model specification: Directory - cfg_files
    inputs{1, crun} = cellstr(fullfile(WORK_DIR, 'models', sprintf('sub-%s', subject)));
    
    % --- run 1 ---
    % fMRI model specification: Scans - cfg_files
    inputs{2, crun} = cellstr(fullfile(...
        DATA_DIR,...
        sprintf(subdir_pattern, subject),...
        sprintf(file_pattern, subject, 1)));
    
    % fMRI model specification: Multiple conditions - cfg_files
    inputs{3, crun} = cellstr(fullfile(...
        WORK_DIR, 'spm_inputs', sprintf(conditions_pattern, subject, 1)));
    
    % fMRI model specification: Multiple regressors - cfg_files
    inputs{4, crun} = cellstr(fullfile(...
        WORK_DIR, 'spm_inputs', sprintf(regressors_pattern, subject, 1)));
    
    % --- run 2 ---
    % fMRI model specification: Scans - cfg_files
    inputs{5, crun} = cellstr(fullfile(...
        DATA_DIR,...
        sprintf(subdir_pattern, subject),...
        sprintf(file_pattern, subject, 2)));
    
    % fMRI model specification: Multiple conditions - cfg_files
    inputs{6, crun} = cellstr(fullfile(...
        WORK_DIR, 'spm_inputs', sprintf(conditions_pattern, subject, 2)));
    
    % fMRI model specification: Multiple regressors - cfg_files
    inputs{7, crun} = cellstr(fullfile(...
        WORK_DIR, 'spm_inputs', sprintf(regressors_pattern, subject, 2)));
    
    % fMRI model specification: Explicit mask - cfg_files
    inputs{8, crun} = cellstr(fullfile(...
        DATA_DIR,...
        sprintf(subdir_pattern, subject),...
        sprintf(mask_pattern, subject)));
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
