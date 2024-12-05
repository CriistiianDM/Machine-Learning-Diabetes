
# section for error

sudo /sbin/vboxconfig
vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: Building VirtualBox kernel modules.
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    linux-headers-amd64 linux-headers-6.1.0-23-amd64
This system is currently not set up to build kernel modules.
Please install the Linux kernel "header" files matching the current kernel
for adding new hardware support to the system.
The distribution packages containing the headers are probably:
    linux-headers-amd64 linux-headers-6.1.0-23-amd64

There were problems setting up VirtualBox.  To re-start the set-up process, run
  /sbin/vboxconfig
as root.  If your system is using EFI Secure Boot you may need to sign the
kernel modules (vboxdrv, vboxnetflt, vboxnetadp, vboxpci) before you can load
them. Please see your Linux system's documentation for more information.?

## Fixed
```
    sudo apt update
    sudo apt install linux-headers-$(uname -r)
    sudo /sbin/vboxconfig
```

Note: Que perdida de tiempo es intentar hacer docker-machine con virtualbox. Lo mejor es instalar microservidores para esta tarea configurando con shh.(Quizas sea por debian)