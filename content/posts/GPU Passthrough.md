+++
title = "GPU Passthrough with 2 identical GPUs"
description = """
  "My personal Notes on my current GPU passthrough setup"
  """
date = 2020-03-04T15:58:26+08:00
lastmod = 2023-12-01T03:04:53+01:00
tags = ["Tech"]
draft = false
+++

## Pre-fly check {#pre-fly-check}

Here are briefly some essential requirements for proceeding. <br/>
****Document as much as possible before doing anything or buying any components****, especially the MOBO, and make sure that the hardware you have support GPU passhtrough. <br/>


### Hardware {#hardware}

I have a custom build desktop computer with the following specs: <br/>

-   MOBO: Asus Prime X570-P <br/>
-   CPU: Ryzen 9 3900x <br/>
-   GPU: 2xRX580 <br/>
-   RAM: Corsair Vengeance 2x16Gb <br/>

The MOBO must support IOMMU and have usable IOMMU groups, otherwise you should look into IOMMU group patching which is kinda of a big pain in the ass. <br/>
The CPU must support hardware virtualization (check on the BIOS settings), you can find it named differently depending on the CPU brand. <br/>


#### Help Sources {#help-sources}

Here you are some useful guide and sources that I have look up during the process. <br/>

-   [Arch Wiki](<https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF#Using_identical_guest_and_host_GPUs>) <br/>
-   [Nice Blog Post](<https://dividebyzer0.gitlab.io/GPUpassthrough.html>) <br/>


## Here we go {#here-we-go}


### Enable IOMMU {#enable-iommu}

Enable IOMMU support by setting the correct kernel parameter <br/>

-   For Intel CPUs (VT-d) set intel_iommu=on. <br/>
-   For AMD CPUs (AMD-Vi), it is on if kernel detects IOMMU hardware support from BIOS. <br/>

If you use GRUB bootloader modify the \`GRUB_CMD_LINUX_DEFAULT\`. <br/>

```bash
GRUB_CMDLINE_LINUX_DEFAULT='amd_iommu=on iommu=pt quiet resume=UUID=13a46783-44ea-4be4-acf1-19005617583e loglevel=3 video=efifb:off'
```

Go ahead and reboot. Then check that your changes had been applied looking at the IOMMU groups using the following script: <br/>

```bash
#!/bin/bash
shopt -s nullglob
for g in $(find /sys/kernel/iommu_groups/* -maxdepth 0 -type d | sort -V); do
    echo "IOMMU Group ${g##*/}:"
    for d in $g/devices/*; do
        echo -e "\t$(lspci -nns ${d##*/})"
    done;
done;
```

The output should look like this: <br/>

```bash
IOMMU Group 0:
    00:01.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 1:
    00:01.1 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge [1022:1483]
IOMMU Group 2:
    00:01.2 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge [1022:1483]
IOMMU Group 3:
    00:02.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 4:
    00:03.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 5:
    00:03.1 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse GPP Bridge [1022:1483]
IOMMU Group 6:
    00:04.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 7:
    00:05.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 8:
    00:07.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 9:
    00:07.1 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B] [1022:1484]
IOMMU Group 10:
    00:08.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Host Bridge [1022:1482]
IOMMU Group 11:
    00:08.1 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Internal PCIe GPP Bridge 0 to bus[E:B] [1022:1484]
IOMMU Group 12:
    00:14.0 SMBus [0c05]: Advanced Micro Devices, Inc. [AMD] FCH SMBus Controller [1022:790b] (rev 61)
    00:14.3 ISA bridge [0601]: Advanced Micro Devices, Inc. [AMD] FCH LPC Bridge [1022:790e] (rev 51)
IOMMU Group 13:
    00:18.0 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 0 [1022:1440]
    00:18.1 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 1 [1022:1441]
    00:18.2 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 2 [1022:1442]
    00:18.3 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 3 [1022:1443]
    00:18.4 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 4 [1022:1444]
    00:18.5 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 5 [1022:1445]
    00:18.6 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 6 [1022:1446]
    00:18.7 Host bridge [0600]: Advanced Micro Devices, Inc. [AMD] Matisse/Vermeer Data Fabric: Device 18h; Function 7 [1022:1447]
IOMMU Group 14:
    01:00.0 Non-Volatile memory controller [0108]: Samsung Electronics Co Ltd NVMe SSD Controller 980 [144d:a809]
IOMMU Group 15:
    02:00.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse Switch Upstream [1022:57ad]
IOMMU Group 16:
    03:02.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a3]
IOMMU Group 17:
    03:05.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a3]
IOMMU Group 18:
    03:06.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a3]
IOMMU Group 19:
    03:08.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a4]
    07:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP [1022:1485]
    07:00.1 USB controller [0c03]: Advanced Micro Devices, Inc. [AMD] Matisse USB 3.0 Host Controller [1022:149c]
    07:00.3 USB controller [0c03]: Advanced Micro Devices, Inc. [AMD] Matisse USB 3.0 Host Controller [1022:149c]
IOMMU Group 20:
    03:09.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a4]
    08:00.0 SATA controller [0106]: Advanced Micro Devices, Inc. [AMD] FCH SATA Controller [AHCI mode] [1022:7901] (rev 51)
IOMMU Group 21:
    03:0a.0 PCI bridge [0604]: Advanced Micro Devices, Inc. [AMD] Matisse PCIe GPP Bridge [1022:57a4]
    09:00.0 SATA controller [0106]: Advanced Micro Devices, Inc. [AMD] FCH SATA Controller [AHCI mode] [1022:7901] (rev 51)
IOMMU Group 22:
    04:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
    04:00.1 Audio device [0403]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere HDMI Audio [Radeon RX 470/480 / 570/580/590] [1002:aaf0]
IOMMU Group 23:
    05:00.0 Ethernet controller [0200]: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller [10ec:8168] (rev 15)
IOMMU Group 24:
    06:00.0 Network controller [0280]: Intel Corporation Wi-Fi 6 AX200 [8086:2723] (rev 1a)
IOMMU Group 25:
    0a:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
    0a:00.1 Audio device [0403]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere HDMI Audio [Radeon RX 470/480 / 570/580/590] [1002:aaf0]
IOMMU Group 26:
    0b:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse PCIe Dummy Function [1022:148a]
IOMMU Group 27:
    0c:00.0 Non-Essential Instrumentation [1300]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Reserved SPP [1022:1485]
IOMMU Group 28:
    0c:00.1 Encryption controller [1080]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse Cryptographic Coprocessor PSPCPP [1022:1486]
IOMMU Group 29:
    0c:00.3 USB controller [0c03]: Advanced Micro Devices, Inc. [AMD] Matisse USB 3.0 Host Controller [1022:149c]
IOMMU Group 30:
    0c:00.4 Audio device [0403]: Advanced Micro Devices, Inc. [AMD] Starship/Matisse HD Audio Controller [1022:1487]
```


### Isolating the GPU {#isolating-the-gpu}

This task result way simpler if you have two different GPU, such as amd and nvdia cards. In my case unfortunately I have 2 practically identical RX580. <br/>
As you see in the IOMMU groups they share the same ID. <br/>

This is the first one: <br/>

```bash
IOMMU Group 22:
04:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
04:00.1 Audio device [0403]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere HDMI Audio [Radeon RX 470/480 / 570/580/590] [1002:aaf0]
```

This is the second one <br/>

```bash
IOMMU Group 22:
IOMMU Group 25:
    0a:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
    0a:00.1 Audio device [0403]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere HDMI Audio [Radeon RX 470/480 / 570/580/590] [1002:aaf0]
```

In this case a workaround should be used, overriding the binding procedure. <br/>
Go ahead and create a script in \`/usr/local/bin/vfio-pci-override.sh\`. Using your device identifier. <br/>

```bash
IOMMU Group 22:
#!/bin/sh
DEVS="0000:04:00.0 0000:04:00.1"

if [ ! -z "$(ls -A /sys/class/iommu)" ]; then
    for DEV in $DEVS; do
        echo "vfio-pci" > /sys/bus/pci/devices/$DEV/driver_override
    done
fi

modprobe -i vfio-pci
```

****Do not forget**** to install teh script. To do so: <br/>

Edit /etc/mkinitcpio.conf: <br/>

-   Add modconf to the HOOKS array and \`/usr/local/bin/vfio-pci-override.sh\` to the FILES array. <br/>

Edit /etc/modprobe.d/vfio.conf: <br/>

-   Add the following line: install vfio-pci \`/usr/local/bin/vfio-pci-override.sh\` <br/>

Regenerate the initramfs and reboot. <br/>

After rebooting in order to check if the changes were successful use the command \`lspci -nnnk\`, look for the correct identifier. <br/>
The output should look something like: <br/>

```bash
04:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Ellesmere [Radeon RX 470/480/570/570X/580/580X/590] [1002:67df] (rev e7)
    Subsystem: Micro-Star International Co., Ltd. [MSI] Radeon RX 580 ARMOR 8G OC [1462:3418]
    Kernel driver in use: vfio-pci
    Kernel modules: amdgpu
```

Note that vfio-pci is in use. <br/>
After this you GPU can be passed through your favorite virtual machine manager. I use virt-manager. <br/>


### VM setup {#vm-setup}

Install \`qemu\`, \`libvirt\`, \`virt-manager\`. <br/>

