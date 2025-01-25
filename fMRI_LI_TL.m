%% ========================================================================

clear 
project = 'VHMC';
maindir = pwd;
id = strfind(maindir,'/');
datadir = [maindir(1:id(end) - 6),'/Data','/fMRI','/',project,'/resting-task_state','/derivatives','/ica.gift'];
file = dir([datadir,'/','ica__sub*_component*.nii']);
mask = [maindir(1:id(end) - 6),'/Data','/fMRI','/',project,'/resting-task_state','/derivatives','/ica.gift','/ica.networks/LRN','/LRN_wo_networks.nii'];

addpath(genpath('/Users/victor/Documents/spm12'));
addpath(genpath([maindir(1:id(end)),'libraries']));

LI_table(1,1) = {'participant'};
LI_table(1,2) = {'LI_raw'};

for i = 1:length(file)
    disp(['start sub-0',num2str(i)]);
    image = [file(i).folder,'/',file(i).name];
    LI_table(i+1,1) = {['sub-0',num2str(i)]};

    out = struct('A',[image,',27'],'B1',mask,'C1',2,'thr1',-1,'vc',0,'outfile',[datadir,'/','li.txt']);
    LI(out);
    result = readtable([datadir,'/','li.txt']);
    LI_table(i+1,2) = {table2array(result(1,6))};
    
    delete([datadir,'/','li.txt']);
    clear result
    close all
    
    try 
        delete([pwd,'/LI_r_spmT_0001.nii']);cllc
        delete([pwd,'/LI_masking.ps']);
    
    catch   
        continue
    end
end

save('/Volumes/Projects_1/Results/fMRI/VHMC/LI_network_wo.mat','LI_table')
