% create stick contrasts on first level for each subject
% delete previously existing contrasts
% set OVERRIDE_SUBDIR to traverse folder other than WORK_DIR/models

config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;
work_subdir = 'models_xm_90';

subjects = {
    '03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14';...
    '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

% 11 columns per session in design matrix (excluding regressors)
% need stick contrast for each one except the last
% these will be replicated & scaled (batch menu setting)
n_contrasts = 10;
contrast_vectors = eye(n_contrasts);

contrast_names = {
    'movie-erotic',...
    'rest-erotic',...
    'movie-fear',...
    'rest-fear',...
    'movie-joy',...
    'rest-joy',...
    'movie-neutral',...
    'rest-neutral',...
    'movie-sadness',...
    'rest-sadness',...
    };

nrun = length(subjects); % enter the number of runs here
jobfile = {'contrast_manager_1st_stick_90_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(21, nrun);
for crun = 1:nrun
    % Contrast Manager: Select SPM.mat - cfg_files
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, work_subdir, sprintf('sub-%s', subjects{crun}), 'SPM.mat'));
    
    in = 1; % input number - there are 2 open inputs per contrast
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
