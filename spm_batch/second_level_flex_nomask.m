config = ini2struct('../movrest_config.ini');
WORK_DIR = config.default.work_dir;

dir_1st_lvl = 'models_xm';  % use 1st lvl masked with fmriprep's mask
dir_2nd_lvl = 'flex_factorial_xm1_noxm2';

subjects = {'03'; '04'; '05'; '06'; '07'; '08'; '09'; '10'; '11'; '12'; '14'; '16'; '17'; '18'; '19'; '20'; '21'; '22'; '23'; '25'; '26'; '27'};

mask_used = cellstr('');  % this should mean no mask

% size of needed matrices
n_conditions = 20;
n_subjects = length(subjects);

n_cells = n_conditions * n_subjects;

% create empty factor matrix and scans cellstr
factor_matrix = ones(n_cells, 4);
scans = cell(n_cells, 1);

% fill them in
row_number = 1;
for cn = 1:n_conditions
    for sn = 1:n_subjects
        
        sub_folder = sprintf('sub-%s', subjects{sn});
        con_fname = sprintf('con_%04d.nii', cn);
        con_path = fullfile(WORK_DIR, dir_1st_lvl, sub_folder, con_fname);
        
        factor_matrix(row_number, :) = [row_number cn sn 1];  % [1 cn sn 1]
        scans{row_number} = con_path;
        row_number = row_number + 1;
    end
end


nrun = 1; % enter the number of runs here
jobfile = {'second_level_flex_job.m'};  % reusing this, but changing input
jobs = repmat(jobfile, 1, nrun);
inputs = cell(5, nrun);
for crun = 1:nrun
    % Factorial design specification: Directory - cfg_files
    inputs{1, crun} = cellstr(fullfile(...
        WORK_DIR, 'models2', dir_2nd_lvl));
    
    % Factorial design specification: Scans - cfg_files
    inputs{2, crun} = scans;
    
    % Factorial design specification: Factor matrix - cfg_entry
    inputs{3, crun} = factor_matrix;
     
    % Factorial design specification: Explicit Mask - cfg_files
    inputs{4, crun} = mask_used;
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
