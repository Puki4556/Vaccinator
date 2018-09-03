# Vaccinator

## Prologue
I have been working in cyber security from 2012.  
Over the years, I got tired of always being one step behind the attackers.  
This tool is supposed to prevent some of the malware to run in first place on my organisation.  
This tool provides a way to vaccinate the workstation from those malware.  

## About the project
This project supposed to vaccinate your workstation from malware.  
In an attempt to evade analysis and being detected, malware often scans for:  
1) The presence of a forensics-related process running
2) The presence of VM Indicators.
3) The presence of Sandbox Indicators.
Mostly if the malware detects one of the above it will change it's behaviour: suspended/closed/'act naturally' (Do only legitimate stuff) so it won't be detected.

# VaccOnOff
A tool that detects a kind of malwares ends/suspends their process when they detect a forensics process running.  
https://github.com/DuckInCyber/Vaccinator/tree/master/VaccOnOff

# VaccOnce
In this part of the project we are building a tool which will run once on the computer and will make the machine look like a sandbox analysis guest machine so malware will detect it and “choose” not to operate.
