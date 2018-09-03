# VaccOnce
### TL;DR 
The first part of the project is a tool that supposed to detect malware that attempts to hide itself from forensic tools.
In this part of the project we are building a tool which will run once on the computer and will make the machine look like a sandbox analysis guest machine so malware will detect it and “choose” not to operate
There is a version for Ubuntu (written by Dor Alt) and a version for Windows (written by me).

## Prologue.
When you install and configure a sandbox (I am used to work with Cuckoo) you are setting up an analysis guest machine that samples the behavior of a file. One of the most important things you need to do is making the analysis guest machine that sample the behavior of the file to look like a legit, real-life machine.
Why is that? 
Because a malware doesn't want to be discovered, once someone identifies it as a malware, the chance of successfully attacking and further distributing is dropped significantly.
One of the main things that can detect a malware is a sandbox, therefore, If it classifies the computer as a sandbox or virtual it will probably shutdown itself or act legitimately.

## The purpose.
Due to those ideas, is that if we will make our normal computers look like part of a sandbox or virtual environment, every malware which evades sandboxes will not run on our workstations.
By performing these, we will “Vaccinate” out computers from those malware type.
## How it works.
A malware can detect that the environment is a sandbox or a virtual one in many ways, really many ways. There are more simple ways like checking the presence of certain files, services, process, registry keys, wmi keys, etc. There are more complex ways like monitor the mouse movements and more.

### What we didn't do in this version.
if we want to make our computer look like a virtual computer absolutely, we need to hook the system APIs calls and return the values we want.
We are not going to do that in this version. Why?
1) Because it’s a lot of work.
2) Because we don’t have a QA team. Don’t let anyone without a QA team to change your api calls. Take it as a general rule of thumb.

### What we DID do.
we started from the more simple things like creating files and services.
In the next versions we will change more stuff like Registry keys.
#### What is the risk.
We are changing stuff in the operating system. For now, it's just creating files and services so it's not much of a risk, but in the future we will change more complex stuff. This is why the next version takes time, we're testing very carefully what we do, everything we write, and we’re running on our computers as well. 
Anyway, when we will add things that are a little more risky, we will give you the option to not activate them.
#### What's in the future.
new versions, new contributors, even just ideas (That’s you!) and the last phase of the project (stay tuned).

Thanks, Maor Levi and Dor Alt
