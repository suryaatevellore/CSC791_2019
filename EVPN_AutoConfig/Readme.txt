Before running the script, make sure that the containers have already been created using the tool.
A sample adjacency matrix has been provided ( autoRRs.txt ). If you are specifying a new file, please make sure of the following naming convention:
1) Name of spines should start with S
2) Name of leaves should start with L
3) As of now, the script does not work properly if RR's are not specified. So add a column for RR's. The RR can be connected anywhere.


Environment : 
python > 3.5

Steps to run the script
1) Go to adjacency_matrix.py and make sure that the DIRECTORY PATH variable is set to the location of the rnd_lab folder. As of now the variable is set to 
/home/RND-TOOL/rnd_lab. If this is correct there is no need to touch the variable.
2) The tenant file should be placed in the scripts folder inside rnd_lab. A sample of the tenant file has been added in the EVPN_Autoconfig folder. 
If you are thinking of specifying a new file, please use the sample tenant file as a base. The formatting of the file is very important.
3) Now run the script with python sudo auto_config.py or python3 auto_config.py
4) Watch the magic unfold ! 


Future Work
1) Work towards a object oriented approach, where each leaf, spine is represented as an object
2) Multi threading
