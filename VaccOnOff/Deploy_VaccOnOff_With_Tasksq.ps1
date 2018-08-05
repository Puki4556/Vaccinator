
####################### Stuff you need to change ###########################
# get the list of computers
$comps = Get-Content "C:\comps.txt"

# !!!!!! This value must be identical to the value in the Task_creater script !!!!!!!
$TaskDescr = "onoff"

# Path to the VaccOnOff script
$ps1Path = "C:\path\to\script\task_creater_VaccOnOff.ps1"
###########################################################################
foreach($comp in $comps)
{
    #$comp = $comp.name
    if(Test-Connection $comp -Count 1)
    {
        Write-Host $comp

        # config the winrm if not config
        Invoke-WmiMethod -ComputerName $comp -Class win32_process -name create -ArgumentList "cmd.exe /c winrm qc -q" >> $null

        # execute the script on the other computer
        # the script creates a task
        Invoke-Command -ComputerName $comp -FilePath $ps1Path >> $null
        sleep -Seconds 1

        # run the task
        schtasks /RUN /S $comp /I /TN $TaskDescr ## Put here the task name frome the task_creater ps1
        sleep -Seconds 1

        # delete the task
        schtasks /DELETE /S $comp /F /TN $TaskDescr ## Put here the task name frome the task_creater ps1
    }
} 
