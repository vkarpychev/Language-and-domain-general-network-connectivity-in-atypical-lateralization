% List of open inputs
% Factorial design specification: Directory - cfg_files
% Factorial design specification: Scans - cfg_files

clear 
project = 'VHMC';
maindir = pwd;
id = strfind(maindir,'/');
datadir = [maindir(1:id(end) - 6),'/Data','/fMRI','/',project,'/resting-task_state','/derivatives','/ica.gift/'];

folder = dir([datadir,'ica__sub*_component_ica_s1_.nii']);
inputs = strcat(folder(1).folder,'/',{folder(:).name}');
addpath(genpath('/Users/victor/Documents/spm12/'));
savepath

% the exact numbers of the cognitive networks
networks = {'aDMN','CON','rFPN','DAN','lFPN','pDMN','SN','LRN'};
n_networks = [3 4 14 19 20 24 26 27]; 

for crun = n_networks
    try
        if isfolder([datadir,'ica.networks/',char(networks(n_networks == crun))]) == 0    
           mkdir([datadir,'ica.networks/',char(networks(n_networks == crun))]);
        end
        inputs_network = strcat(inputs,',',num2str(crun));
        output_network = cellstr([datadir,'ica.networks/',char(networks(n_networks == crun))]);
        spm_network = cellstr([datadir,'ica.networks/',char(networks(n_networks == crun)),'/SPM.mat']);
        matlabbatch = fMRI_ICA_activation_job(inputs_network,output_network,spm_network);
        spm_jobman('run', matlabbatch);
        
        close all
        clear inputs_network output_network spm_network 
        cd(maindir)
    catch
        continue
    end

end
