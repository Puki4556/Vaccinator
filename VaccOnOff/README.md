# VaccOnOff

![gif](https://media.giphy.com/media/ncve7z4oPPURO/source.gif)

### The script is not intended to prevent malware. it is intended to detect.  
It starts the Vacc on and then off ;)

## The purpose
This script is supposed to detect malware that attempts to hide itself from forensic tools.  
This kind of malware ends/suspends their process when they detect a forensics-related process running  
Evasive malware can look for other indicators than processes (i.e. registry keys), but this will be covered in the next version.  
A list of process names is available at: https://github.com/DuckInCyber/Vaccinator  

Change the name of the exe to the names on the list https://github.com/DuckInCyber/Vaccinator/blob/master/Process%20Names.txt (or use your own names).
You can use the exe I have uploaded and multiplied it and change the names to the names on the list.   https://github.com/DuckInCyber/Vaccinator/blob/master/simple_process_for_name_changing.exe  
Put all the exe files you want in a folder.  

Written by DuckInCyber  
Date 31/7/18  
Version 0.0.1  

## How it works
This tool have deployer scripts (Deploy_VaccOnOff_With_Tasksq.ps1 and Task_Creater_VaccOnOff.ps1) and a deployed script (VaccOnOff.ps1).  
In my experience, the best way to run a ps1 script on severl remote computers is to create a schedule task on the computer and remotly activate it.  
Task_Creater_VaccOnOff.ps1 - creates the schedule task that will run the VaccOnOff.ps1 from a network share.  
VaccOnOff.ps1 - this script will run on the endpoints. 
Deploy_VaccOnOff_With_Tasksq.ps1 - the deployer.

## What the VaccOnOff.ps1 does
By the order:  
1) Getting the suspended process so I will be able to find the new suspended processes.  
2) Create a listener to closing processes.  
3) Starting the forensics-related processes.  
4) Getting the suspended process so I will be able to find the new suspended processes.  
5) Stopping the forensics-related processes.  
6) Moving log (Closed processes log) files to the output folder.  
7) Exporting the difference of the suspened processes.  
8) Changing the permissions on the output folder (This is very important because you don't want the "EVERYONE" will have full access to this files. you don't want the attacker to be able to change this files or watch then and know we got him).  

## What you need?
1) Ports 445 and 135 from the deployer station to the endpoints.
2) A network share for the input and output. This share need to have 3 folders:  
2.1) Tools - You need a network path with read permissions for "Everyone" or "Domain Computers".  
        In this folder you need to have all the executable files that will run on the endpoint.  
2.2) Input - You need a network path with read permissions for "Everyone" or "Domain Computers".  
        In this folder you need to have the VaccOnOff.ps1 file (copy the script to the path when you activates the script and delete it from there later).  
2.3) Output - You need a network path with full control permissions for "Everyone" or "Domain Computers".  
        Result output path.
3) A domain user or group that will have permissions to read the output.
4) A client local admin user to run the deployer.ps1 with his permissions, you can use a Domain admin.

# Please Read The Scripts
Every variable you will need to change is marked in a section that start with:  
####################### Stuff you need to change ###########################

Change this variables with yours values
