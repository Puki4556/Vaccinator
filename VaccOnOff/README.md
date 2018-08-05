## VaccOnOff

This script is supposed to detect malware that attempts to hide from forensic tools.  
This kind of malwares ends/suspends their process when they detect a forensics process running  
There are another things except detectingprocesses, but.... next version (-; .  
A list of processes name process names is available at: https://github.com/DuckInCyber/Vaccinator  

Change the name of the exe to the names on the list (or use your own names).  
Pull all the exe files you want in a folder  

Written by DuckInCyber  
Date 31/7/18  
Version 0.0.1  

# How it works
This tool have a deployer scripts (Deploy_VaccOnOff_With_Tasksq.ps1 and Task_Creater_VaccOnOff.ps1) and a deployed script (VaccOnOff.ps1).  
In my expirince, the best way to run a ps1 script on a remote 
This tool have 3 scripts:  
1) VaccOnOff.ps1 - this script will run on the endpoints.  
2) 
