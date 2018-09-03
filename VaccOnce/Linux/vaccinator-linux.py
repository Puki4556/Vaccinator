'''
__author__ = "Dor Alt"
__email__ = "agentzex@gmail.com"

This program is part of the Vaccinator project: https://github.com/DuckInCyber/Vaccinator
Please look there for more instructions.

Vaccinator for Linux systems, spoofing the system to look like a VmWare vm

How to use:

-s start             start the linux vaccination process
-k kill              kill and revert the vaccination process


Usage: python vaccinator-linux.py -s


'''

import os
from vm_service_template import vm_service
import psutil
import shutil
import zipfile
import spoofmac
from optparse import OptionParser
import logging
import platform


# Checking if sudo
print "* Checking if running as root... *"
try:
    with open("/etc/init.d/test.txt", "w") as file:
        file.write("")
except Exception, e:
    if e.args[1] == 'Permission denied':
        print "Please run this program as root", "error"
        raise Exception("Please run this program as root")

print "* Root confirmed *"

arch = platform.architecture()[0]

# Init for logger
current_dir = os.getcwd()
bin_dir = current_dir + os.sep + "bin"
if not os.path.exists(current_dir + os.sep + "logs"):
    os.mkdir(current_dir + os.sep + "logs")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler(current_dir + os.sep + "logs" + os.sep + 'Logger.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s",
                              "%d-%m-%Y %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_command_line_arguments():
    parser = OptionParser("usage: %prog -s")
    parser.add_option("-s", "--start", dest="start", action="store_true", help="start the linux vaccination process")
    parser.add_option("-k", "--kill", dest="kill", action="store_true", help="kill and revert the vaccination process")
    (options, args) = parser.parse_args()

    if options.start and options.kill:
        parser.error("You must select either -s or -k flags")

    if not options.start and not options.kill:
        parser.error("You must select either -s or -k flags")

    if options.start:
        return "start"
    else:
        return "kill"


def spoof_mac_addresses():
    print_and_log("* trying to spoof mac address *", "info")
    interfaces_gen = spoofmac.find_interfaces()
    found_interfaces = []
    for interface in interfaces_gen:
        found_interfaces.append(interface)

    vmware_mac = "00:0c:29:"
    for interface in found_interfaces:
        splitted = interface[2].split(":")[3:]
        mac = ":".join(splitted)
        mac = vmware_mac + mac
        spoofmac.set_interface_mac(interface[1], mac)

    with open(current_dir + os.sep + "logs" + os.sep + "interfaces", "w") as file:
        for interface in interfaces_gen:
            file.write(interface[1] + " " + interface[2] + "\n")

    print_and_log("* mac address spoofed successfully *", "info")


def revert_mac_addresses():
    print_and_log("* trying to revert mac addresses back to default *", "info")

    with open(current_dir + os.sep + "logs" + os.sep + "interfaces", "r") as file:
        for line in file:
            line = line.strip()
            splitted = line.split()
            interface = splitted[0]
            mac = splitted[1]
            spoofmac.set_interface_mac(interface, mac)

    print_and_log("* mac addresses were reverted to default *", "info")


def get_pids(running_processes):
    c = psutil.process_iter()
    pids = []
    list_of_processes = []
    for process in c:
        list_of_processes.append((process.name(), process.pid))
    list_of_processes = sorted(list_of_processes)

    for process_name in running_processes:
        for process in list_of_processes:
            if process[0] == process_name:
                pids.append(process[1])
    return pids


def unzip_bin():
    with zipfile.ZipFile("bin.zip", "r") as zip:
        zip.extractall("bin")


def create_paths_and_run_processes():
    print_and_log("* trying to create vmware paths and to run processes *", "info")
    running_processes = []

    # Giving permissions
    for file in os.listdir(bin_dir):
        os.chmod(bin_dir + os.sep + file, 0o777)

    # Copying to directories and starting vmware executables
    if not os.path.exists("/usr/sbin"):
        os.makedirs("/usr/sbin/")
    shutil.copy(bin_dir + os.sep + "vmware-vmblock-fuse", "/usr/sbin/")
    pid = os.fork()
    if pid == 0:
        os.system("nohup /usr/sbin/vmware-vmblock-fuse &")
        running_processes.append("vmware-vmblock-fuse")

    shutil.copy(bin_dir + os.sep + "vmtoolsd", "/usr/sbin/")

    shutil.copy(bin_dir + os.sep + "tpvmlpd2", "/usr/sbin/")
    pid = os.fork()
    if pid == 0:
        os.system("nohup /usr/sbin/tpvmlpd2 &")
        running_processes.append("tpvmlpd2")

    shutil.copy(bin_dir + os.sep + "16-vmwgfx", "/usr/sbin/")
    pid = os.fork()
    if pid == 0:
        os.system("nohup /usr/sbin/16-vmwgfx &")
        running_processes.append("16-vmwgfx")

    if not os.path.exists("/usr/lib/vmware-tools/sbin64/"):
        os.makedirs("/usr/lib/vmware-tools/sbin64/")
    pid = os.fork()
    if pid == 0:
        os.system("nohup /usr/lib/vmware-tools/sbin64/vmtoolsd &")
        running_processes.append("vmtoolsd")

    if not os.path.exists("/usr/lib/vmware-tools/"):
        os.makedirs("/usr/lib/vmware-tools/")

    if not os.path.exists("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx"):
        os.makedirs("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx")

    if not os.path.exists("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx"):
        os.makedirs("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx")

    if not os.path.exists("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock"):
        os.makedirs("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock/")

    if not os.path.exists("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock"):
        os.makedirs("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock/")

    pids = get_pids(running_processes)
    print_and_log("* finished creating paths and starting processes *", "info")
    print_and_log("$$ Running PIDs are: " + str(pids) + " $$", "info")

    with open(current_dir + os.sep + "logs" + os.sep + "pids" , "w") as file:
        file.write("\n".join(pids))


def remove_paths():
    print_and_log("* trying to remove vmware paths *", "info")
    if os.path.exists("/usr/sbin/vmware-vmblock-fuse"):
        os.remove("/usr/sbin/vmware-vmblock-fuse")
    if os.path.exists("/usr/sbin/vmtoolsd"):
        os.remove("/usr/sbin/vmtoolsd")
    if os.path.exists("/usr/sbin/tpvmlpd2"):
        os.remove("/usr/sbin/tpvmlpd2")
    if os.path.exists("/usr/sbin/16-vmwgfx"):
        os.remove("/usr/sbin/16-vmwgfx")
    if os.path.exists("/usr/lib/vmware-tools"):
        shutil.rmtree("/usr/lib/vmware-tools")
    if os.path.exists("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx"):
        shutil.rmtree("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx")
    if os.path.exists("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx"):
        shutil.rmtree("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx")
    if os.path.exists("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock/"):
        shutil.rmtree("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock/")
    if os.path.exists("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock/"):
        shutil.rmtree("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock/")

    print_and_log("* finished removing vmware paths *", "info")


def create_services():
    print_and_log("* creating vmware services... *", "info")
    with open("/etc/init.d/vmware-tools", "w") as file:
        file.write(vm_service)
    os.chmod("/etc/init.d/vmware-tools", 0o777)

    with open("/etc/init.d/vmware-tools-thinprint", "w") as file:
        file.write(vm_service)
    os.chmod("/etc/init.d/vmware-tools-thinprint", 0o777)

    print_and_log("* vmware services were created successfully *", "info")


def remove_services():
    print_and_log("* removing vmware services... *", "info")
    os.remove("/etc/init.d/vmware-tools")
    os.remove("/etc/init.d/vmware-tools-thinprint")
    print_and_log("* vmware services were removed successfully *", "info")


def print_and_log(log_line, level):
    print log_line
    if level == "info":
        logger.info(log_line)
    elif level == "error":
        logger.error(log_line)


def kill_processes():
    print_and_log("* trying to kill old vmware proccesses *", "info")
    pids = []
    with open(current_dir + os.sep + "logs" + os.sep + "pids", "r") as file:
        for line in file:
            pids.append(line.strip())

    os.system("sudo kill " + " ".join(pids))
    print_and_log("* processes " + " ".join(pids) + " were killed *", "info")


def spoof_dmidecode():
    try:
        print_and_log("* trying to replace dmidecode *", "info")
        os.system("mv /usr/sbin/dmidecode /usr/sbin/dmidecode_org")
        if os.path.exists("/usr/sbin/dmidecode_org"):
            if arch == "32bit":
                shutil.copy(bin_dir + os.sep + "dmidecode_32", "/usr/sbin/dmidecode")
            else:
                shutil.copy(bin_dir + os.sep + "dmidecode_64", "/usr/sbin/dmidecode")

        print_and_log("* dmidecode was replaced successfully *", "info")
    except Exception, e:
        print_and_log("* failed to replace dmidecode. Error was: " + str(e) + " *", "error")


def revert_to_original_dmidecode():
    try:
        print_and_log("* trying to revert back to original dmidecode *", "info")
        if os.path.exists("/usr/sbin/dmidecode_org"):
            os.system("mv /usr/sbin/dmidecode_org /usr/sbin/dmidecode")

        print_and_log("* dmidecode was reverted to original successfully *", "info")
    except Exception, e:
        print_and_log("* failed to revert dmidecode back to original. Error was: " + str(e) + " *", "error")


def spoof_lscpu():
    try:
        print_and_log("* trying to replace lscpu *", "info")
        os.system("mv /usr/sbin/lscpu /usr/sbin/lscpu_org")
        if os.path.exists("/usr/sbin/lscpu_org"):
            if arch == "32bit":
                shutil.copy(bin_dir + os.sep + "lscpu_32", "/usr/sbin/lscpu")
            else:
                shutil.copy(bin_dir + os.sep + "lscpu_64", "/usr/sbin/lscpu")

        print_and_log("* lscpu was replaced successfully *", "info")
    except Exception, e:
        print_and_log("* failed to replace lscpu. Error was: " + str(e) + " *", "error")



def revert_to_original_lscpu():
    try:
        print_and_log("* trying to revert back to original lscpu *", "info")
        if os.path.exists("/usr/sbin/lscpu_org"):
            os.system("mv /usr/sbin/lscpu_org /usr/sbin/lscpu")

        print_and_log("* lscpu was reverted to original successfully *", "info")
    except Exception, e:
        print_and_log("* failed to revert lscpu back to original. Error was: " + str(e) + " *", "error")




if __name__ == "__main__":
    operation = parse_command_line_arguments()

    if operation == "start":
        print_and_log("* starting vaccination process *", "info")
        try:
            unzip_bin()
            spoof_mac_addresses()
            create_paths_and_run_processes()
            create_services()
            spoof_dmidecode()
            spoof_lscpu()
            print_and_log("* finished vaccination process *", "info")
        except Exception, e:
            print_and_log("* Error occurred: " + str(e) + " *", "error")

    else:
        print_and_log( "* reverting vaccination process *", "info")
        try:
            kill_processes()
            remove_services()
            remove_paths()
            revert_mac_addresses()
            revert_to_original_dmidecode()
            revert_to_original_lscpu()
            print_and_log("* finished reverting vaccination process *", "info")
        except Exception, e:
            print_and_log("* Error occurred: " + str(e) + " *", "error")
