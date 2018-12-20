config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;

subjects = {'03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14'; '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

mean_fd = load(fullfile(WORK_DIR, 'spm_inputs', 'mean_fd.mat'));
% use mean_fd.mean_fd to access actual vector

% DROP SUBJECT 08 - optional -
% now would require dropping from subjects & mean fd
% con_files(6) = [];
% mean_fd.mean_fd(6) = [];
% ----------------------------

folder_names = {'rest_vs_mov', 'mov_vs_rest',...
                'rest_ero_vs_rest_neu', 'rest_fear_vs_rest_neu',...
                'rest_neu_vs_rest_ero', 'rest_neu_vs_rest_fear'};
con_numbers = {1, 2, 3, 4, 5, 6};

nrun = length(folder_names);

jobfile = {'second_level_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(3, nrun);
for crun = 1:nrun
    % Factorial design specification: Directory - cfg_files
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, 'models2', folder_names{crun}));
    
    % Factorial design specification: Scans - cfg_files
    inputs{2, crun} = listcon(subjects, WORK_DIR, con_numbers{crun});
    
    % Factorial design specification: Vector - cfg_entry
    inputs{3, crun} = mean_fd.mean_fd;
end

spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});


function con_files = listcon(subs, wdir, cn)
% LISTCON build list of con files (in the form of a cellstring)
    n_subs = length(subs);
    con_files = cell(n_subs, 1);
    for n = 1:n_subs
        con_files{n, 1} = fullfile(...
            wdir,...
            'models',...
            sprintf('sub-%s', subs{n}),...
            sprintf('con_%04d.nii', cn));
    end
end