##########################################################################################################
#                                                                                                        #
#                                             The VaccOnce                                               #
#                                                                                                        #
#                                                                                                        #
# This script is supposed to make your computer look like it is part of a sandbox/virtual environment.   #
# For more Details:                                                                                      #
# https://github.com/DuckInCyber/Vaccinator/blob/master/VaccOnce/Readme.md                               #
#                                                                                                        #
# Written by DuckInCyber                                                                                 #
# Date 2/9/18                                                                                            #
# Version 0.0.1                                                                                          #
#                                                                                                        #
##########################################################################################################

####################### Stuff you need to change ###########################
# The output log file of what the script created or deleted.
$log_file_path = "c:\log.log"
############################################################################


# files to create
$files_to_create = @(
"C:\windows\system32\vboxdisp.dll",
"C:\windows\system32\vboxhook.dll",
"C:\windows\system32\vboxmrxnp.dll",
"C:\windows\system32\vboxogl.dll",
"C:\windows\system32\vboxoglarrayspu.dll",
"C:\windows\system32\vboxoglcrutil.dll",
"C:\windows\system32\vboxoglerrorspu.dll",
"C:\windows\system32\vboxoglfeedbackspu.dll",
"C:\windows\system32\vboxoglpackspu.dll",
"C:\windows\system32\vboxoglpassthroughspu.dll",
"C:\windows\system32\vboxservice.exe",
"C:\windows\system32\vboxtray.exe",
"C:\windows\system32\VBoxControl.exe",
"c:\sample.exe",
"c:\malware.exe",
"C:\tracer\mdare32_0.sys",
"C:\tracer\fortitracer.exe",
"C:\manual\sunbox.exe",
"c:\agent.py",
"c:\agent.pyw",
"c:\analyzer.py",
"c:\cuckoo\dll",
"c:\pipe\cuckoo",
"c:\SandboxStarter.exe")

# Folders to create
$folders_to_create = @(
"C:\Program Files\oracle\virtualbox guest additions",
"C:\Program Files\VMWare")

# Services to create
$srv_to_create = @(
"VirtualBox",
"VMWare",
"VMTools",
"Vmhgfs",
"VMMEMCTL",
"Vmmouse",
"Vmrawdsk",
"Vmusbmouse",
"Vmvss",
"Vmscsi",
"Vmxnet",
"vmx_svga",
"Vmware Tools",
"Vmware Physical Disk Helper Service")

# Create a log array
$log = @()

# Creating files
foreach ($file in $files_to_create)
{
    if (!(test-path $file))
    {
        $folder = $file.Substring(0,($file.LastIndexOf('\')))
        if(test-path $folder)
        {
            $file | Out-File -FilePath $file -Force
            $log += ("file" + "," + "$file")
        }
        else
        {
            new-item -path $folder -ItemType Directory
            $file | Out-File -FilePath $file -Force
            $log += ("file" + "," + "$file")
        }
    }
}

# Creating folders
foreach ($folder in $folders_to_create)
{
    if (!(test-path $folder))
    {
        New-Item -Path $folder -ItemType Directory -Force
        $log += ("folder" + "," + "$folder")
    }
}

# Creating services
$current_services = Get-Service | select -ExpandProperty name
foreach ($service in $srv_to_create)
{
    if (!($current_services | ?{$_ -eq "$service"}))
    {
        New-Service -Name $service -DisplayName $service -BinaryPathName "C:\Windows\In_The_Next_Version_There_Will_Be_A_Real_File.exe"
        $log += ("service" + "," + "$service")
    }
}

# Export log file
$log | Out-File -FilePath $log_file_path -Encoding utf8 -Force
