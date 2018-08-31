import os
from vm_service_template import vm_service
import psutil
import shutil
import zipfile
import spoofmac
from optparse import OptionParser



current_dir = os.getcwd()


def parse_command_line_arguments():
    parser = OptionParser("usage: %prog -s")
    parser.add_option("-s", "--start", dest="start", action="store_true", help="start the linux vaccination process")
    parser.add_option("-k", "--kill", dest="kill", action="store_true", help="kill and reset the vaccination process")
    (options, args) = parser.parse_args()

    if options.start and options.kill:
        parser.error("You must select either -s or -k options")

    if not options.start and not options.kill:
        parser.error("You must select either -s or -k options")

    if options.start:
        return "start"
    else:
        return "kill"

def spoof_mac_addresses():
    print "* Spoofing mac address *"

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

    print "* mac address spoofed successfully *"

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


def create_paths():
    print "* Creating vmware paths and running processes *"
    running_processes = []
    bin_dir = current_dir + os.sep + "bin"

    with zipfile.ZipFile("bin.zip", "r") as zip:
        zip.extractall("bin")

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

    if not os.path.exists("/usr/lib/vmware-tools/bin64"):
        os.makedirs("/usr/lib/vmware-tools/bin64")

    if not os.path.exists("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx"):
        os.makedirs("/lib/modules/4.15.0-29-generic/kernel/drivers/gpu/drm/vmwgfx")

    if not os.path.exists("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx"):
        os.makedirs("/lib/modules/4.15.0-33-generic/kernel/drivers/gpu/drm/vmwgfx")

    if not os.path.exists("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock/"):
        os.makedirs("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock/")

    if not os.path.exists("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock/"):
        os.makedirs("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock/")

    if not os.path.exists("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock"):
        os.makedirs("/lib/modules/4.15.0-29-generic/kernel/net/vmw_vsock")

    if not os.path.exists("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock"):
        os.makedirs("/lib/modules/4.15.0-33-generic/kernel/net/vmw_vsock")

    pids = get_pids(running_processes)
    print "* Finished creating paths and starting processes *"
    print "* Running PIDs are: " + str(pids) + " *"

    #todo - save pids in a file and kill them if asked


def create_services():
    print "* Creating vmware services... *"

    with open("/etc/init.d/vmware-tools", "w") as file:
        file.write(vm_service)
    os.chmod("/etc/init.d/vmware-tools", 0o777)

    with open("/etc/init.d/vmware-tools-thinprint", "w") as file:
        file.write(vm_service)
    os.chmod("/etc/init.d/vmware-tools-thinprint", 0o777)

    print "* vmware services were created successfully *"


def check_sudo():
    print "* Checking if running as root... *"
    try:
        os.rename("/etc/b", "etc/bbb")
    except Exception, e:
        if e.args[1] == 'Permission denied':
            raise Exception("Please run this program as root")

    print "* Root confirmed *"


if __name__ == "__main__":
    operation = parse_command_line_arguments()
    check_sudo()

    if operation == "start":
        print "* starting vaccination process *"
        # spoof_mac_addresses()
        create_paths()
        create_services()

    else:
        print "* resetting vaccination process *"

