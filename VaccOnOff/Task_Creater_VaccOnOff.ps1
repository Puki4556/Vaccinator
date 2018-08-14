## This script need to rub as administrator on the remote machine and create a schedule task.
## The task will run the desired from a network path as system
## All the credit for this script deserve to this guy https://www.verboon.info/2013/12/powershell-creating-scheduled-tasks-with-powershell-version-3/

####################### Stuff you need to change ###########################
## Task name
## Change the name!!!!!
# !!!!!! This value must be identical to the value in the deployer script !!!!!!!
$TaskName = "onoff"

# The description of the task
$TaskDescr = $TaskName

#the network path to the script
$TaskScript = "\\net_share\folder_with_everyone_read_permission\vaccinator.ps1"

############################################################################


# The Task Action command
$TaskCommand = "c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe"
# The Task Action command argument
$TaskArg = "-WindowStyle Hidden -NonInteractive -Executionpolicy bypass -file $TaskScript"

# The time when the task starts, for demonstration purposes we run it 1 minute after we created the task
$TaskStartTime = [datetime]::Now.AddMinutes(2) 

# attach the Task Scheduler com object
$service = new-object -ComObject("Schedule.Service")
# connect to the local machine. 
# http://msdn.microsoft.com/en-us/library/windows/desktop/aa381833(v=vs.85).aspx
$service.Connect()
$rootFolder = $service.GetFolder("\")

$TaskDefinition = $service.NewTask(0) 
$TaskDefinition.RegistrationInfo.Description = "$TaskDescr"
$TaskDefinition.Settings.Enabled = $true
$TaskDefinition.Settings.AllowDemandStart = $true

$triggers = $TaskDefinition.Triggers
#http://msdn.microsoft.com/en-us/library/windows/desktop/aa383915(v=vs.85).aspx
$trigger = $triggers.Create(2) 
$trigger.StartBoundary = $TaskStartTime.ToString("yyyy-MM-dd'T'HH:mm:ss")
$trigger.Enabled = $true

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa381841(v=vs.85).aspx
$Action = $TaskDefinition.Actions.Create(0)
$action.Path = "$TaskCommand"
$action.Arguments = "$TaskArg"

#http://msdn.microsoft.com/en-us/library/windows/desktop/aa381365(v=vs.85).aspx
$rootFolder.RegisterTaskDefinition("$TaskName",$TaskDefinition,6,"System",$null,5)
# The Task Action command
$TaskCommand = "c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe"
# The Task Action command argument
$TaskArg = "-WindowStyle Hidden -NonInteractive -Executionpolicy unrestricted -file $TaskScript"
 
# The time when the task starts, for demonstration purposes we run it 1 minute after we created the task
$TaskStartTime = [datetime]::Now.AddMinutes(1) 
 
# attach the Task Scheduler com object
$service = new-object -ComObject("Schedule.Service")
# connect to the local machine. 
# http://msdn.microsoft.com/en-us/library/windows/desktop/aa381833(v=vs.85).aspx
$service.Connect()
$rootFolder = $service.GetFolder("\")
 
$TaskDefinition = $service.NewTask(0) 
$TaskDefinition.RegistrationInfo.Description = "$TaskDescr"
$TaskDefinition.Settings.Enabled = $true
$TaskDefinition.Settings.AllowDemandStart = $true
 
$triggers = $TaskDefinition.Triggers
#http://msdn.microsoft.com/en-us/library/windows/desktop/aa383915(v=vs.85).aspx
$trigger = $triggers.Create(1) # Creates a "One time" trigger
$trigger.StartBoundary = $TaskStartTime.ToString("yyyy-MM-dd'T'HH:mm:ss")
$trigger.Enabled = $true
 
# http://msdn.microsoft.com/en-us/library/windows/desktop/aa381841(v=vs.85).aspx
$Action = $TaskDefinition.Actions.Create(0)
$action.Path = "$TaskCommand"
$action.Arguments = "$TaskArg"
 
#http://msdn.microsoft.com/en-us/library/windows/desktop/aa381365(v=vs.85).aspx
$rootFolder.RegisterTaskDefinition("$TaskName",$TaskDefinition,6,"System",$null,5)
