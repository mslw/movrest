% create stick contrasts on first level for each subject
% delete previously existing contrasts
% set OVERRIDE_SUBDIR to traverse folder other than WORK_DIR/models

config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;
work_subdir = 'models';

% ugly way to change subdir to avoid creating another script or using 
% a function if only folder changes
if exist('OVERRIDE_SUBDIR', 'var')
    work_subdir = OVERRIDE_SUBDIR;
    disp(['Using folder ' fullfile(WORK_DIR, work_subdir)]);
end

subjects = {
    '03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14';...
    '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

% 21 columns per session in design matrix (excluding regressors)
% need stick contrast for each one except the last
% these will be replicated & scaled (batch menu setting)
n_contrasts = 20;
contrast_vectors = eye(n_contrasts);

% build contrast names
categories = {'erotic', 'joy', 'fear', 'sadness', 'neutral'}; % conf. make_multiple_conditions
contrast_names = cell(n_contrasts,1);
for n = 1:length(categories)
    category = categories{n};
    cn = 4*n - 4; % condition number (movie + 3 x rest per category)
    contrast_names{cn+1} = strcat('movie-', category);
    contrast_names{cn+2} = strcat('rest-post-', category, '-1');
    contrast_names{cn+3} = strcat('rest-post-', category, '-2');
    contrast_names{cn+4} = strcat('rest-post-', category, '-3');
end

nrun = length(subjects); % enter the number of runs here
jobfile = {'contrast_manager_1st_stick_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(41, nrun);
for crun = 1:nrun
    % Contrast Manager: Select SPM.mat - cfg_files
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, work_subdir, sprintf('sub-%s', subjects{crun}), 'SPM.mat'));
    
    in = 1; % input number - there are 3 open inputs per contrast
    for cn = 1:n_contrasts
        % Contrast Manager: Name - cfg_entry
        inputs{in+1, crun} = contrast_names{cn};
        %Contrast Manager: Weights vector - cfg_entry
        inputs{in+2, crun} = contrast_vectors(cn,:);
        in = in + 2;
    end
    
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
