This repository includes Python script used to pre and post-process needed files for HMI-PRED workflow.

Codes

HMI Preprocess_GetPDBChains.py  >> We have mined PDB structures relevant to the virus of interest from the literature. Structure chains belonging to these structures were extracted using this code and written into a file. Each column (chain identifier) is an input to HMI-PRED when merged with PDB ID.
HMI Process_FaultyFiles.py  >> Some queries returned a different formatted HMI-PRED for unknown reasons. This code is used to modify such output files to the expected format.
HMI Process_MergeResults.py >> This code is used to process final result files and merge them into a single folder for further analysis.

Files

all_pdbs.xlsx >> Contains all extracted PDBs from the literature.
cmv_chains >> Viral chains associated with CMV virus as outputted by *HMI Preprocess_GetPDBChains.py* file.
ebv_chains >> Viral chains associated with EBV virus as outputted by *HMI Preprocess_GetPDBChains.py* file.
h1n1_chains >> Viral chains associated with H1N1 virus as outputted by *HMI Preprocess_GetPDBChains.py* file.
h5n1_chains >> Viral chains associated with H5N1 virus as outputted by *HMI Preprocess_GetPDBChains.py* file.
hsv_chains >> Viral chains associated with HSV-1 virus as outputted by *HMI Preprocess_GetPDBChains.py* file.
Cytomegalovirus >> HMI-PRED output for CMV.
Eppstein-Bar >> HMI-PRED output for EBV.
H1N1 >> HMI-PRED output for H1N1.
H5N1 >> HMI-PRED output for H5N1.
HIV >> HMI-PRED output for HIV.

