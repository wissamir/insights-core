from insights.combiners.grub_conf import GrubConf, BootLoaderEntries
from insights.parsers.grub_conf import (
    Grub1Config,
    Grub2Config,
    Grub2EFIConfig,
    Grub1EFIConfig,
    BootLoaderEntries as BLE,
)
from insights.parsers.grubenv import GrubEnv
from insights.parsers.ls import LSlanFiltered
from insights.parsers.installed_rpms import InstalledRpms
from insights.parsers.cmdline import CmdLine
from insights.tests import context_wrap
import pytest

GRUB1_TEMPLATE = """
# grub.conf generated by anaconda
#
# Note that you do not have to rerun grub after making changes to this file
# NOTICE:  You have a /boot partition.  This means that
#          all kernel and initrd paths are relative to /boot/, eg.
#          root (hd0,0)
#          kernel /vmlinuz-version ro root=/dev/mapper/VolGroup-lv_root
#          initrd /initrd-[generic-]version.img
#boot=/dev/sda
default=0
timeout=5
splashimage=(hd0,0)/grub/splash.xpm.gz
hiddenmenu
title Red Hat Enterprise Linux 6 (2.6.32-642.el6.x86_64)
        root (hd0,0)
        kernel /vmlinuz-2.6.32-642.el6.x86_64 {kernel_boot_options} ro root=/dev/mapper/VolGroup-lv_root intel_iommu=off rd_NO_LUKS LANG=en_US.UTF-8 rd_NO_MD rd_LVM_LV=VolGroup/lv_swap SYSFONT=latarcyrheb-sun16 crashkernel=auto rd_LVM_LV=VolGroup/lv_root  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
        initrd /initramfs-2.6.32-642.el6.x86_64.img
title Red Hat Enterprise Linux 6 (2.6.32-642.el6.x86_64-2)
        root (hd0,0)
        kernel /vmlinuz-2.6.32-642.el6.x86_64 {kernel_boot_options} ro root=/dev/mapper/VolGroup-lv_root intel_iommu=on rd_NO_LUKS LANG=en_US.UTF-8 rd_NO_MD rd_LVM_LV=VolGroup/lv_swap SYSFONT=latarcyrheb-sun16 crashkernel=auto rd_LVM_LV=VolGroup/lv_root  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
        initrd /initramfs-2.6.32-642.el6.x86_64.img
title Red Hat Enterprise Linux 6 (2.6.32-642.el6.x86_64-2)
        root (hd0,0)
        kernel /vmlinuz-2.6.32-642.el6.x86_64 {kernel_boot_options} ro root=/dev/mapper/VolGroup-lv_root rd_NO_LUKS LANG=en_US.UTF-8 rd_NO_MD rd_LVM_LV=VolGroup/lv_swap SYSFONT=latarcyrheb-sun16 crashkernel=auto rd_LVM_LV=VolGroup/lv_root  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
        initrd /initramfs-2.6.32-642.el6.x86_64.img
""".strip()  # noqa

# rhel-7
GRUB2_TEMPLATE = """
#
# DO NOT EDIT THIS FILE
#
# It is automatically generated by grub2-mkconfig using templates
# from /etc/grub.d and settings from /etc/default/grub
#

### BEGIN /etc/grub.d/00_header ###
set pager=1

terminal_output console
### END /etc/grub.d/00_header ###

### BEGIN /etc/grub.d/00_tuned ###
set tuned_params=""
### END /etc/grub.d/00_tuned ###

### BEGIN /etc/grub.d/01_users ###

### END /etc/grub.d/01_users ###

### BEGIN /etc/grub.d/10_linux ###
menuentry 'Red Hat Enterprise Linux Server (3.10.0-327.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce' {
        load_video
        set gfxpayload=keep
        insmod gzio
        insmod part_msdos
        insmod xfs
        set root='hd0,msdos1'
        if [ x$feature_platform_search_hint = xy ]; then
          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint='hd0,msdos1'  860a7b56-dbdd-498a-b085-53dc93e4650b
        else
          search --no-floppy --fs-uuid --set=root 860a7b56-dbdd-498a-b085-53dc93e4650b
        fi
        linux16 /vmlinuz-3.10.0-327.el7.x86_64 %s root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8
        initrd16 /initramfs-3.10.0-327.el7.x86_64.img
}
menuentry 'Red Hat Enterprise Linux Server (0-rescue-9f20b35c9faa49aebe171f62a11b236f) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-9f20b35c9faa49aebe171f62a11b236f-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce' {
        load_video
        insmod gzio
        insmod part_msdos
        insmod xfs
        set root='hd0,msdos1'
        if [ x$feature_platform_search_hint = xy ]; then
          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint='hd0,msdos1'  860a7b56-dbdd-498a-b085-53dc93e4650b
        else
          search --no-floppy --fs-uuid --set=root 860a7b56-dbdd-498a-b085-53dc93e4650b
        fi
        linux16 /vmlinuz-0-rescue-9f20b35c9faa49aebe171f62a11b236f %s root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet
        initrd16 /initramfs-0-rescue-9f20b35c9faa49aebe171f62a11b236f.img
}
""".strip()  # noqa

GRUB2_TEMPLATE_BLSCFG = """
#
# DO NOT EDIT THIS FILE
#
# It is automatically generated by grub2-mkconfig using templates
# from /etc/grub.d and settings from /etc/default/grub
#

### BEGIN /etc/grub.d/00_header ###
set pager=1

terminal_output console
### END /etc/grub.d/00_header ###

### BEGIN /etc/grub.d/00_tuned ###
set tuned_params=""
### END /etc/grub.d/00_tuned ###

### BEGIN /etc/grub.d/01_users ###

### END /etc/grub.d/01_users ###
insmod blscfg
blscfg
if [ -s $prefix/grubenv ]; then
  load_env
fi

if [ -z "${kernelopts}" ]; then
  set kernelopts="root=/dev/mapper/rhel-root ro crashkernel=auto resume=/dev/mapper/rhel-swap rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet transparent_hugepage=never "
fi
""".strip()  # noqa

GRUB2_TEMPLATE_NO_BLSCFG = """
#
# DO NOT EDIT THIS FILE
#
# It is automatically generated by grub2-mkconfig using templates
# from /etc/grub.d and settings from /etc/default/grub
#

### BEGIN /etc/grub.d/00_header ###
set pager=1

terminal_output console
### END /etc/grub.d/00_header ###

### BEGIN /etc/grub.d/00_tuned ###
set tuned_params=""
### END /etc/grub.d/00_tuned ###

### BEGIN /etc/grub.d/01_users ###

### END /etc/grub.d/01_users ###
### BEGIN /etc/grub.d/10_linux ###
menuentry 'Red Hat Enterprise Linux Server (4.18.0-240.el8.x86_64) 8.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce' {
        load_video
        set gfxpayload=keep
        insmod gzio
        insmod part_msdos
        insmod xfs
        set root='hd0,msdos1'
        if [ x$feature_platform_search_hint = xy ]; then
          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint='hd0,msdos1'  860a7b56-dbdd-498a-b085-53dc93e4650b
        else
          search --no-floppy --fs-uuid --set=root 860a7b56-dbdd-498a-b085-53dc93e4650b
        fi
        linux16 /vmlinuz-4.18.0-240.el8.x86_64 %s root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8
        initrd16 /initramfs-4.18.0-240.el8.x86_64.img
}
menuentry 'Red Hat Enterprise Linux Server (0-rescue-9f20b35c9faa49aebe171f62a11b236f) 8.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-9f20b35c9faa49aebe171f62a11b236f-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce' {
        load_video
        insmod gzio
        insmod part_msdos
        insmod xfs
        set root='hd0,msdos1'
        if [ x$feature_platform_search_hint = xy ]; then
          search --no-floppy --fs-uuid --set=root --hint-bios=hd0,msdos1 --hint-efi=hd0,msdos1 --hint-baremetal=ahci0,msdos1 --hint='hd0,msdos1'  860a7b56-dbdd-498a-b085-53dc93e4650b
        else
          search --no-floppy --fs-uuid --set=root 860a7b56-dbdd-498a-b085-53dc93e4650b
        fi
        linux16 /vmlinuz-0-rescue-9f20b35c9faa49aebe171f62a11b236f %s root=/dev/mapper/rhel-root ro crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet
        initrd16 /initramfs-0-rescue-9f20b35c9faa49aebe171f62a11b236f.img
}
""".strip()  # noqa

GRUB2_EFI_CFG = """
### BEGIN /etc/grub.d/10_linux ###
menuentry 'Red Hat Enterprise Linux Server (3.10.0-514.16.1.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {
    load_video
    set gfxpayload=keep
    insmod gzio
    insmod part_gpt
    insmod xfs
    set root='hd0,gpt2'
    if [ x$feature_platform_search_hint = xy ]; then
      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe
    else
      search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe
    fi
    linuxefi /vmlinuz-3.10.0-514.16.1.el7.x86_64 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8
    initrdefi /initramfs-3.10.0-514.16.1.el7.x86_64.img
}
menuentry 'Red Hat Enterprise Linux Server (3.10.0-514.10.2.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {
    load_video
    set gfxpayload=keep
    insmod gzio
    insmod part_gpt
    insmod xfs
    set root='hd0,gpt2'
    if [ x$feature_platform_search_hint = xy ]; then
      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe
    else
      search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe
    fi
    linuxefi /vmlinuz-3.10.0-514.10.2.el7.x86_64 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8
    initrdefi /initramfs-3.10.0-514.10.2.el7.x86_64.img
}
menuentry 'Red Hat Enterprise Linux Server (3.10.0-514.el7.x86_64) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-514.el7.x86_64-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {
    load_video
    set gfxpayload=keep
    insmod gzio
    insmod part_gpt
    insmod xfs
    set root='hd0,gpt2'
    if [ x$feature_platform_search_hint = xy ]; then
      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe
    else
      search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe
    fi
    linuxefi /vmlinuz-3.10.0-514.el7.x86_64 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet LANG=en_US.UTF-8
    initrdefi /initramfs-3.10.0-514.el7.x86_64.img
}
menuentry 'Red Hat Enterprise Linux Server (0-rescue-f1340b5dd6ee4c26b587621566111421) 7.3 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-0-rescue-f1340b5dd6ee4c26b587621566111421-advanced-9727cab4-12c2-41a8-9527-9644df34e586' {
    load_video
    insmod gzio
    insmod part_gpt
    insmod xfs
    set root='hd0,gpt2'
    if [ x$feature_platform_search_hint = xy ]; then
      search --no-floppy --fs-uuid --set=root --hint-bios=hd0,gpt2 --hint-efi=hd0,gpt2 --hint-baremetal=ahci0,gpt2  d80fa96c-ffa1-4894-9282-aeda37f0befe
    else
      search --no-floppy --fs-uuid --set=root d80fa96c-ffa1-4894-9282-aeda37f0befe
    fi
    linuxefi /vmlinuz-0-rescue-f1340b5dd6ee4c26b587621566111421 root=/dev/mapper/rhel-root ro rd.luks.uuid=luks-a40b320e-0711-4cd6-8f9e-ce32810e2a79 rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet
    initrdefi /initramfs-0-rescue-f1340b5dd6ee4c26b587621566111421.img
}

### END /etc/grub.d/10_linux ###
""".strip()  # noqa

GRUB1_EFI_CFG = """
# grub.conf generated by anaconda
#
# Note that you do not have to rerun grub after making changes to this file
# NOTICE:  You have a /boot partition.  This means that
#          all kernel and initrd paths are relative to /boot/, eg.
#          root (hd0,1)
#          kernel /vmlinuz-version ro root=/dev/mapper/VolGroup-lv_root
#          initrd /initrd-[generic-]version.img
#boot=/dev/mpathap1
default=0
timeout=5
splashimage=(hd0,1)/grub/splash.xpm.gz
hiddenmenu
title Red Hat Enterprise Linux (2.6.32-71.el6.x86_64)
        root (hd0,1)
        kernel /vmlinuz-2.6.32-71.el6.x86_64 ro root=/dev/mapper/VolGroup-lv_root rd_LVM_LV=VolGroup/lv_root rd_LVM_LV=VolGroup/lv_swap rd_NO_LUKS rd_NO_MD rd_NO_DM LANG=en_US.UTF-8 SYSFONT=latarcyrheb-sun16 KEYBOARDTYPE=pc KEYTABLE=us crashkernel=auto rhgb quiet
        initrd /initramfs-2.6.32-71.el6.x86_64.img
""".strip()  # noqa

SYS_FIRMWARE_DIR_NOEFI = """
/sys/firmware:
total 0
drwxr-xr-x.  5 0 0 0 May 30 11:50 .
dr-xr-xr-x. 13 0 0 0 May 30 11:50 ..
drwxr-xr-x.  5 0 0 0 May 30 11:50 acpi
drwxr-xr-x.  3 0 0 0 May 30 11:51 dmi
drwxr-xr-x.  7 0 0 0 May 30 12:31 memmap

/sys/firmware/acpi:
total 0
drwxr-xr-x. 5 0 0    0 May 30 11:50 .
drwxr-xr-x. 5 0 0    0 May 30 11:50 ..
drwxr-xr-x. 6 0 0    0 May 30 12:31 hotplug
drwxr-xr-x. 2 0 0    0 May 30 12:31 interrupts
-r--r--r--. 1 0 0 4096 May 30 12:31 pm_profile
drwxr-xr-x. 3 0 0    0 May 30 11:50 tables
""".strip()

SYS_FIRMWARE_DIR_EFI = """
/sys/firmware:
total 0
drwxr-xr-x.  5 0 0 0 May 30 11:50 .
dr-xr-xr-x. 13 0 0 0 May 30 11:50 ..
drwxr-xr-x.  5 0 0 0 May 30 11:50 acpi
drwxr-xr-x.  3 0 0 0 May 30 11:51 dmi
drwxr-xr-x.  7 0 0 0 May 30 12:31 efi

/sys/firmware/efi:
total 0
drwxr-xr-x. 5 0 0    0 May 30 11:50 .
drwxr-xr-x. 5 0 0    0 May 30 11:50 ..
""".strip()

INSTALLED_RPMS_V1 = """
grub-0.97-94.el6.x86_64                     Mon Jan  8 18:35:25 2018
libreport-compat-2.0.9-24.el6.x86_64        Mon Jan  8 18:32:59 2018
make-3.81-20.el6.x86_64                     Mon Jan  8 18:31:49 2018
""".strip()

INSTALLED_RPMS_V2 = """
grub2-2.02-0.44.el7.x86_64                  Wed May 10 14:10:30 2017
libwbclient-4.4.4-12.el7_3.x86_64           Wed May 10 14:08:10 2017
xorg-x11-drv-vmmouse-13.0.0-12.el7.x86_64   Wed May 10 14:10:36 2017
""".strip()

CMDLINE_V1 = """
ro root=/dev/mapper/vg_rhel6box-lv_root rd_NO_LUKS LANG=en_US.UTF-8 rd_LVM_LV=vg_rhel6box/lv_swap rd_LVM_LV=vg_rhel6box/lv_root rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=129M@0M  KEYBOAR DTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet
""".strip()  # noqa

CMDLINE_V2 = """
BOOT_IMAGE=/vmlinuz-3.10.0-514.10.2.el7.x86_64 root=/dev/mapper/vg_system-lv_root ro crashkernel=auto rd.lvm.lv=vg_system/lv_root rd.lvm.lv=vg_system/lv_swap rhgb quiet LANG=en_US.UTF-8
""".strip()  # noqa

BOOT_LOADER_ENTRIES_1 = """
title Red Hat Enterprise Linux (4.18.0-80.1.2.el8_0.x86_64) 8.0 (Ootpa)
version 4.18.0-80.1.2.el8_0.x86_64
linux /vmlinuz-4.18.0-80.1.2.el8_0.x86_64
initrd /initramfs-4.18.0-80.1.2.el8_0.x86_64.img $tuned_initrd
options root=/dev/mapper/rhel_vm37--146-root ro crashkernel=auto resume=/dev/mapper/rhel_vm37--146-swap rd.lvm.lv=rhel_vm37-146/root rd.lvm.lv=rhel_vm37-146/swap $tuned_params noapic
id rhel-20190428101407-4.18.0-80.1.2.el8_0.x86_64
grub_users $grub_users
grub_arg --unrestricted
grub_class kernel
""".strip()  # noqa

BOOT_LOADER_ENTRIES_2 = """
title Red Hat Enterprise Linux (4.18.0-32.el8.x86_64) 8.0 (Ootpa)
version 4.18.0-32.el8.x86_64
linux /vmlinuz-4.18.0-32.el8.x86_64
initrd /initramfs-4.18.0-32.el8.x86_64.img
options root=/dev/mapper/rhel_rhel8-root ro elevator=noop no_timer_check crashkernel=auto resume=/dev/mapper/rhel_rhel8-swap rd.lvm.lv=rhel_rhel8/root rd.lvm.lv=rhel_rhel8/swap biosdevname=0 net.ifnames=0 rhgb
id rhel-20181027203430-4.18.0-32.el8.x86_64
grub_users $grub_users
grub_arg --unrestricted
grub_class kernel
""".strip()  # noqa

BOOT_LOADER_ENTRIES_3 = """
title Red Hat Enterprise Linux (4.18.0-305.el8.x86_64) 8.4 (Ootpa)
version 4.18.0-305.el8.x86_64
linux /vmlinuz-4.18.0-305.el8.x86_64
initrd /initramfs-4.18.0-305.el8.x86_64.img $tuned_initrd
options $kernelopts $tuned_params
id rhel-20210429130346-4.18.0-305.el8.x86_64
grub_users $grub_users
grub_arg --unrestricted
grub_class kernel
""".strip()

GRUBENV_WITH_TUNED_PARAMS = """
# GRUB Environment Block
saved_entry=295e1ba1696e4fad9e062f096f92d147-4.18.0-305.el8.x86_64
kernelopts=root=/dev/mapper/root_vg-lv_root ro crashkernel=auto resume=/dev/mapper/root_vg-lv_swap rd.lvm.lv=root_vg/lv_root rd.lvm.lv=root_vg/lv_swap console=tty0 console=ttyS0,115200 noapic
boot_success=0
boot_indeterminate=2
tuned_params=transparent_hugepages=never
tuned_initrd=
###############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
""".strip()  # noqa


def test_grub1_only1():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    cmdline = CmdLine(context_wrap(CMDLINE_V1))
    result = GrubConf(grub1, None, None, None, None, None, cmdline, None, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-2.6.32-642.el6.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-2.6.32-642.el6.x86_64.img'
    assert result.is_kdump_iommu_enabled is True
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert len(result.get_grub_cmdlines()) == 3
    assert result.version == 1
    assert result.is_efi is False


def test_grub1_cmdline():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    cmdline = CmdLine(context_wrap(CMDLINE_V1))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, None, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-2.6.32-642.el6.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-2.6.32-642.el6.x86_64.img'
    assert result.is_kdump_iommu_enabled is True
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert len(result.get_grub_cmdlines()) == 3
    assert result.version == 1
    assert result.is_efi is False


def test_grub1_efi_cmdline():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    cmdline = CmdLine(context_wrap(CMDLINE_V1))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_EFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, None, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-2.6.32-71.el6.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-2.6.32-71.el6.x86_64.img'
    assert result.is_kdump_iommu_enabled is False
    assert len(result.get_grub_cmdlines()) == 1
    assert result.version == 1
    assert result.is_efi is True


def test_grub1_rpms():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V1))
    cmdline = CmdLine(context_wrap(CMDLINE_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, rpms, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-2.6.32-642.el6.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-2.6.32-642.el6.x86_64.img'
    assert result.is_kdump_iommu_enabled is True
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert len(result.get_grub_cmdlines()) == 3
    assert result.version == 1
    assert result.is_efi is False


def test_grub1_efi_rpms():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V1))
    cmdline = CmdLine(context_wrap(CMDLINE_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_EFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, rpms, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-2.6.32-71.el6.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-2.6.32-71.el6.x86_64.img'
    assert result.is_kdump_iommu_enabled is False
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert len(result.get_grub_cmdlines()) == 1
    assert result.version == 1
    assert result.is_efi is True


def test_grub2_cmdline():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    cmdline = CmdLine(context_wrap(CMDLINE_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, None, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-3.10.0-327.el7.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-3.10.0-327.el7.x86_64.img'
    assert result.is_kdump_iommu_enabled is False
    assert (
        result.get_grub_cmdlines('/vmlinuz-3.10.0')[0].name
        == "'Red Hat Enterprise Linux Server (3.10.0-327.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce'"
    )  # noqa
    assert result.get_grub_cmdlines('test') == []
    assert result.get_grub_cmdlines('') == []
    assert len(result.get_grub_cmdlines()) == 2
    assert result.version == 2
    assert result.is_efi is False


def test_grub2_efi_cmdline():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    cmdline = CmdLine(context_wrap(CMDLINE_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_EFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, None, cmdline, ls_lan, None)
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert result.get_grub_cmdlines('rescue')[0].name.startswith(
        "'Red Hat Enterprise Linux Server (0-rescue"
    )
    assert len(result.get_grub_cmdlines()) == 4
    assert result.version == 2
    assert result.is_efi is True


def test_grub2_rpms():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    cmdline = CmdLine(context_wrap(CMDLINE_V1))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, rpms, cmdline, None, None)
    assert result.kernel_initrds['grub_kernels'][0] == 'vmlinuz-3.10.0-327.el7.x86_64'
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-3.10.0-327.el7.x86_64.img'
    assert result.is_kdump_iommu_enabled is False
    assert (
        result.get_grub_cmdlines('/vmlinuz-3.10.0')[0].name
        == "'Red Hat Enterprise Linux Server (3.10.0-327.el7.x86_64) 7.2 (Maipo)' --class red --class gnu-linux --class gnu --class os --unrestricted $menuentry_id_option 'gnulinux-3.10.0-327.el7.x86_64-advanced-4f80b3d4-90ba-4545-869c-febdecc586ce'"
    )  # noqa
    assert result.get_grub_cmdlines('test') == []
    assert result.get_grub_cmdlines('') == []
    assert len(result.get_grub_cmdlines()) == 2
    assert result.version == 2
    assert result.is_efi is False


def test_grub2_efi_rpms():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub1e = Grub1EFIConfig(context_wrap(GRUB1_EFI_CFG))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    cmdline = CmdLine(context_wrap(CMDLINE_V1))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_EFI))
    result = GrubConf(grub1, grub2, grub1e, grub2e, None, rpms, cmdline, ls_lan, None)
    assert result.kernel_initrds['grub_initrds'][0] == 'initramfs-3.10.0-514.16.1.el7.x86_64.img'
    assert result.get_grub_cmdlines() == result.get_grub_cmdlines('/vmlinuz')
    assert result.get_grub_cmdlines('rescue')[0].name.startswith(
        "'Red Hat Enterprise Linux Server (0-rescue"
    )
    assert len(result.get_grub_cmdlines()) == 4
    assert result.version == 2
    assert result.is_efi is True


def test_get_grub_cmdlines_none():
    grub1 = Grub1Config(context_wrap(GRUB1_TEMPLATE))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    cmdline = CmdLine(context_wrap(CMDLINE_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_EFI))
    with pytest.raises(Exception) as pe:
        GrubConf(grub1, grub2, None, None, None, None, cmdline, ls_lan, None)
    assert "No valid grub configuration is found." in str(pe.value)

    grub1e = Grub1EFIConfig(context_wrap(GRUB1_TEMPLATE))
    grub2e = Grub2EFIConfig(context_wrap(GRUB2_TEMPLATE))
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    with pytest.raises(Exception) as pe:
        GrubConf(None, None, grub1e, grub2e, None, rpms, None, None, None)
    assert "No valid grub configuration is found." in str(pe.value)

    grub2e = Grub2EFIConfig(context_wrap(GRUB2_EFI_CFG))
    with pytest.raises(Exception) as pe:
        GrubConf(grub1, None, grub1e, grub2e, None, rpms, None, None, None)
    assert "No valid grub configuration is found." in str(pe.value)


def test_grub2_grubenv():
    grubenv = GrubEnv(context_wrap(GRUBENV_WITH_TUNED_PARAMS))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE))
    grub_ble1 = BLE(context_wrap(BOOT_LOADER_ENTRIES_1))
    grub_ble2 = BLE(context_wrap(BOOT_LOADER_ENTRIES_2))
    grub_bles = BootLoaderEntries([grub_ble1, grub_ble2], grubenv, None, None)
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(None, grub2, None, None, grub_bles, rpms, None, ls_lan, None)
    assert len(result.get_grub_cmdlines()) == 2
    assert 'noapic' not in result.get_grub_cmdlines()[1]['cmdline']
    assert 'transparent_hugepages' not in result.get_grub_cmdlines()[0]['cmdline']
    assert result.version == 2
    assert not result.is_efi


def test_grub2_grubenv_with_kernelopts():
    grubenv = GrubEnv(context_wrap(GRUBENV_WITH_TUNED_PARAMS))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE_BLSCFG))
    grub_ble1 = BLE(context_wrap(BOOT_LOADER_ENTRIES_1))
    grub_ble2 = BLE(context_wrap(BOOT_LOADER_ENTRIES_2))
    grub_ble3 = BLE(context_wrap(BOOT_LOADER_ENTRIES_3))
    grub_bles = BootLoaderEntries([grub_ble1, grub_ble2, grub_ble3], grubenv, None, None)
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(None, grub2, None, None, grub_bles, rpms, None, ls_lan, None)
    assert len(result.get_grub_cmdlines()) == 3
    assert 'noapic' in result.get_grub_cmdlines()[2]['cmdline']
    assert 'transparent_hugepages' in result.get_grub_cmdlines()[2]['cmdline']
    assert result.version == 2
    assert not result.is_efi


def test_grub2_with_blscfg():
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE_BLSCFG))
    grub_ble1 = BLE(context_wrap(BOOT_LOADER_ENTRIES_1))
    grub_ble2 = BLE(context_wrap(BOOT_LOADER_ENTRIES_2))
    grub_ble3 = BLE(context_wrap(BOOT_LOADER_ENTRIES_3))
    grub_bles = BootLoaderEntries([grub_ble1, grub_ble2, grub_ble3], None, None, None)
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(None, grub2, None, None, grub_bles, rpms, None, ls_lan, None)
    assert len(result.get_grub_cmdlines()) == 3
    assert 'noapic' in result.get_grub_cmdlines()[0]['cmdline']
    assert 'transparent_hugepages' not in result.get_grub_cmdlines()[0]['cmdline']
    assert result.version == 2
    assert not result.is_efi


def test_grub2_boot_loader_entries():
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE_BLSCFG))
    grub_ble1 = BLE(context_wrap(BOOT_LOADER_ENTRIES_1))
    grub_ble2 = BLE(context_wrap(BOOT_LOADER_ENTRIES_2))
    grub_bles = BootLoaderEntries([grub_ble1, grub_ble2], None, None, None)
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(None, grub2, None, None, grub_bles, rpms, None, ls_lan, None)
    assert len(result.get_grub_cmdlines()) == 2
    assert 'noapic' in result.get_grub_cmdlines()[0]['cmdline']
    assert result.version == 2
    assert not result.is_efi


def test_grub2_boot_loader_entries_with_grubenv():
    grubenv = GrubEnv(context_wrap(GRUBENV_WITH_TUNED_PARAMS))
    grub2 = Grub2Config(context_wrap(GRUB2_TEMPLATE_BLSCFG))
    grub_ble1 = BLE(context_wrap(BOOT_LOADER_ENTRIES_1))
    grub_ble3 = BLE(context_wrap(BOOT_LOADER_ENTRIES_3))
    grub_bles = BootLoaderEntries([grub_ble1, grub_ble3], grubenv, None, None)
    rpms = InstalledRpms(context_wrap(INSTALLED_RPMS_V2))
    ls_lan = LSlanFiltered(context_wrap(SYS_FIRMWARE_DIR_NOEFI))
    result = GrubConf(None, grub2, None, None, grub_bles, rpms, None, ls_lan, None)
    assert len(result.get_grub_cmdlines()) == 2
    assert 'noapic' in result.get_grub_cmdlines()[0]['cmdline']
    assert 'transparent_hugepages' in result.get_grub_cmdlines()[0]['cmdline']
    assert 'noapic' in result.get_grub_cmdlines()[1]['cmdline']
    assert 'transparent_hugepages' in result.get_grub_cmdlines()[1]['cmdline']
    assert result.version == 2
    assert not result.is_efi
