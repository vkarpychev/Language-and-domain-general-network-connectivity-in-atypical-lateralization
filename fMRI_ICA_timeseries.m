%% ========================================================================
% loading cPPI data

clear 
project = 'VHMC';
maindir = pwd;
id = strfind(maindir,'/');
addpath(genpath([maindir(1:id(end) - 1),'/libraries/']));
datadir = [maindir(1:id(end) - 6),'/Data','/fMRI','/',project,'/','resting-task_state','/derivatives','/ica.gift'];
file = dir([datadir,'/','*sub*_*timecourses_ica_s1_.nii']);

for crun = 1:length(file)
    
    image_ts = niftiread([datadir,'/',file(crun).name]);
    image_info = niftiinfo([datadir,'/',file(crun).name]);
    ts = image_ts * image_info.MultiplicativeScaling;
    timecourse_cell{crun,1} = ts; 
    
    clear image_ts image_info ts
    
end

save([datadir,'/','timecourse_cell.mat'],'timecourse_cell');
