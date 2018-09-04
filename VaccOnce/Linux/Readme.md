
# Vaccinator - Linux
<pre>
Vaccinator for Linux systems, spoofing the system to look like a VmWare vm
Dependencies:
Please install the followings with "pip install" before running this script:
 - psutil
 - spoofmac


How to use:

-s start             start the linux vaccination process
-k kill              kill and revert the vaccination process
-l spoof_hw          optional - spoof lscpu and dmidecode outputs to look like this machine is a vm


Usage: 

 python vaccinator-linux.py -s -l
 python vaccinator-linux.py -k

</pre>
