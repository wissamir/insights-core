from insights.core.spec_factory import glob_file, simple_file, head, first_file
from functools import partial
from insights.core.context import HostArchiveContext
from insights.specs import Specs

simple_file = partial(simple_file, context=HostArchiveContext)
glob_file = partial(glob_file, context=HostArchiveContext)
first_file = partial(first_file, context=HostArchiveContext)


class InsightsArchiveSpecs(Specs):
    # Client metadata specs/files
    ansible_host = simple_file('/ansible_host')
    blacklisted_specs = first_file(["/blacklisted_specs", "/blacklisted_specs.txt"])
    branch_info = simple_file('/branch_info')
    display_name = simple_file('/display_name')
    tags = simple_file('/tags.json')
    version_info = simple_file('/version_info')

    # Regular collection specs
    abrt_status_bare = simple_file("insights_commands/abrt_status_--bare_True")
    all_installed_rpms = glob_file("insights_commands/rpm_-qa*")
    alternatives_display_python = simple_file("insights_commands/alternatives_--display_python")
    auditctl_rules = simple_file("insights_commands/auditctl_-l")
    auditctl_status = simple_file("insights_commands/auditctl_-s")
    aws_instance_id_doc = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_aws_instance_id_doc"
    )
    aws_instance_id_pkcs7 = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_aws_instance_id_pkcs7"
    )
    awx_manage_check_license = simple_file("insights_commands/awx-manage_check_license")
    awx_manage_print_settings = simple_file(
        "insights_commands/awx-manage_print_settings_INSIGHTS_TRACKING_STATE_SYSTEM_UUID_INSTALL_UUID_TOWER_URL_BASE_AWX_CLEANUP_PATHS_AWX_PROOT_BASE_PATH_LOG_AGGREGATOR_ENABLED_LOG_AGGREGATOR_LEVEL_--format_json"
    )
    azure_instance_id = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_azure_instance_id"
    )
    azure_instance_type = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_azure_instance_type"
    )
    azure_instance_plan = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_azure_instance_plan"
    )
    blkid = simple_file("insights_commands/blkid_-c_.dev.null")
    brctl_show = simple_file("insights_commands/brctl_show")
    ceph_insights = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_ceph_insights"
    )
    ceph_osd_dump = first_file(
        [
            "insights_commands/ceph_osd_dump_-f_json-pretty",
            "insights_commands/ceph_osd_dump_-f_json",
        ]
    )
    ceph_osd_tree = first_file(
        [
            "insights_commands/ceph_osd_tree_-f_json-pretty",
            "insights_commands/ceph_osd_tree_-f_json",
        ]
    )
    ceph_v = simple_file("insights_commands/ceph_-v")
    certificates_enddate = first_file(
        [
            "insights_commands/find_.etc.origin.node_.etc.origin.master_.etc.pki_.etc.ipa_.etc.tower.tower.cert_-type_f_-exec_.usr.bin.openssl_x509_-noout_-enddate_-in_-exec_echo_FileName",
            "insights_commands/find_.etc.origin.node_.etc.origin.master_.etc.pki_.etc.ipa_-type_f_-exec_.usr.bin.openssl_x509_-noout_-enddate_-in_-exec_echo_FileName",
            "insights_commands/find_.etc.origin.node_.etc.origin.master_.etc.pki_-type_f_-exec_.usr.bin.openssl_x509_-noout_-enddate_-in_-exec_echo_FileName",
        ]
    )
    chkconfig = simple_file("insights_commands/chkconfig_--list")
    chronyc_sources = simple_file("insights_commands/chronyc_sources")
    corosync_cmapctl = glob_file("insights_commands/corosync-cmapctl*")
    cpupower_frequency_info = simple_file("insights_commands/cpupower_-c_all_frequency-info")
    date = simple_file("insights_commands/date")
    date_utc = simple_file("insights_commands/date_--utc")
    db2ls_a_c = simple_file("insights_commands/usr.local.bin.db2ls_-a_-c")
    df__al = first_file(["insights_commands/df_-al_-x_autofs", "insights_commands/df_-al"])
    df__alP = first_file(["insights_commands/df_-alP_-x_autofs", "insights_commands/df_-alP"])
    df__li = first_file(["insights_commands/df_-li_-x_autofs", "insights_commands/df_-li"])
    dig_dnssec = simple_file("insights_commands/dig_dnssec_._SOA")
    dig_edns = simple_file("insights_commands/dig_edns_0_._SOA")
    dig_noedns = simple_file("insights_commands/dig_noedns_._SOA")
    dnf_module_list = simple_file("insights_commands/dnf_-C_--noplugins_module_list")
    dmesg = simple_file("insights_commands/dmesg")
    dmidecode = simple_file("insights_commands/dmidecode")
    dmsetup_info = simple_file("insights_commands/dmsetup_info_-C")
    dmsetup_status = simple_file("insights_commands/dmsetup_status")
    docker_info = simple_file("insights_commands/docker_info")
    docker_list_containers = simple_file("insights_commands/docker_ps_--all_--no-trunc")
    docker_list_images = simple_file("insights_commands/docker_images_--all_--no-trunc_--digests")
    dotnet_version = simple_file("insights_commands/dotnet_--version")
    doveconf = simple_file("insights_commands/doveconf")
    ethtool = glob_file("insights_commands/ethtool_*", ignore="ethtool_-.*")
    ethtool_S = glob_file("insights_commands/ethtool_-S_*")
    ethtool_T = glob_file("insights_commands/ethtool_-T_*")
    ethtool_c = glob_file("insights_commands/ethtool_-c_*")
    ethtool_g = glob_file("insights_commands/ethtool_-g_*")
    ethtool_i = glob_file("insights_commands/ethtool_-i_*")
    ethtool_k = glob_file("insights_commands/ethtool_-k_*")
    falconctl_aid = simple_file("insights_commands/opt.CrowdStrike.falconctl_-g_--aid")
    falconctl_backend = simple_file("insights_commands/opt.CrowdStrike.falconctl_-g_--backend")
    falconctl_rfm = simple_file("insights_commands/opt.CrowdStrike.falconctl_-g_--rfm-state")
    falconctl_version = simple_file("insights_commands/opt.CrowdStrike.falconctl_-g_--version")
    fcoeadm_i = simple_file("insights_commands/fcoeadm_-i")
    findmnt_lo_propagation = simple_file("insights_commands/findmnt_-lo_PROPAGATION")
    firewall_cmd_list_all_zones = simple_file("insights_commands/firewall-cmd_--list-all-zones")
    fw_devices = simple_file("insights_commands/fwupdagent_get-devices")
    fw_security = first_file([
        "insights_commands/fwupdmgr_security_--force_--json",
        "insights_commands/fwupdagent_security_--force",
    ])
    flatpak_list = simple_file("insights_commands/flatpak_list")
    gcp_instance_type = simple_file("insights_commands/python_-m_insights.tools.cat_--no-header_gcp_instance_type")
    gcp_license_codes = simple_file("insights_commands/python_-m_insights.tools.cat_--no-header_gcp_license_codes")
    getcert_list = simple_file("insights_commands/getcert_list")
    getconf_page_size = simple_file("insights_commands/getconf_PAGE_SIZE")
    getenforce = simple_file("insights_commands/getenforce")
    getsebool = simple_file("insights_commands/getsebool_-a")
    grubenv = first_file(
        [
            "insights_commands/grub2-editenv_list",
            "/boot/grub2/grubenv",
            "/boot/efi/EFI/redhat/grubenv",
        ]
    )
    grub1_config_perms = first_file(
        [
            "insights_commands/ls_-lH_.boot.grub.grub.conf",
            "insights_commands/ls_-l_.boot.grub.grub.conf",
        ]
    )
    grub_config_perms = first_file(
        [
            "insights_commands/ls_-lH_.boot.grub2.grub.cfg",
            "insights_commands/ls_-l_.boot.grub2.grub.cfg",
        ]
    )
    grubby_default_index = simple_file("insights_commands/grubby_--default-index")
    grubby_default_kernel = simple_file("insights_commands/grubby_--default-kernel")
    gluster_v_info = simple_file("insights_commands/gluster_volume_info")
    installed_rpms = head(all_installed_rpms)
    hostname = simple_file("insights_commands/hostname_-f")
    hostname_default = simple_file("insights_commands/hostname")
    hostname_short = simple_file("insights_commands/hostname_-s")
    httpd_conf = glob_file(
        [
            "/etc/httpd/conf/httpd.conf",
            "/etc/httpd/conf.d/*.conf",
            "/etc/httpd/conf.d/*/*.conf",
            "/etc/httpd/conf.modules.d/*.conf",
        ]
    )
    httpd_conf_scl_httpd24 = glob_file(
        [
            "/opt/rh/httpd24/root/etc/httpd/conf/httpd.conf",
            "/opt/rh/httpd24/root/etc/httpd/conf.d/*.conf",
            "/opt/rh/httpd24/root/etc/httpd/conf.d/*/*.conf",
            "/opt/rh/httpd24/root/etc/httpd/conf.modules.d/*.conf",
        ]
    )
    httpd_conf_scl_jbcs_httpd24 = glob_file(
        [
            "/opt/rh/jbcs-httpd24/root/etc/httpd/conf/httpd.conf",
            "/opt/rh/jbcs-httpd24/root/etc/httpd/conf.d/*.conf",
            "/opt/rh/jbcs-httpd24/root/etc/httpd/conf.d/*/*.conf",
            "/opt/rh/jbcs-httpd24/root/etc/httpd/conf.modules.d/*.conf",
        ]
    )
    httpd_M = glob_file("insights_commands/*httpd*_-M")
    httpd_on_nfs = simple_file(
        "insights_commands/python_-m_insights.tools.cat_--no-header_httpd_on_nfs"
    )
    httpd_V = glob_file("insights_commands/*httpd*_-V")
    initctl_lst = simple_file("insights_commands/initctl_--system_list")
    ip6tables = simple_file("insights_commands/ip6tables-save")
    ip_addr = simple_file("insights_commands/ip_addr")
    ip_addresses = simple_file("insights_commands/hostname_-I")
    ip_route_show_table_all = simple_file("insights_commands/ip_route_show_table_all")
    ip_s_link = first_file(["insights_commands/ip_-s_-d_link", "insights_commands/ip_-s_link"])
    ipcs_m = simple_file("insights_commands/ipcs_-m")
    ipcs_m_p = simple_file("insights_commands/ipcs_-m_-p")
    ipcs_s = simple_file("insights_commands/ipcs_-s")
    iptables = simple_file("insights_commands/iptables-save")
    ipv4_neigh = simple_file("insights_commands/ip_-4_neighbor_show_nud_all")
    ipv6_neigh = simple_file("insights_commands/ip_-6_neighbor_show_nud_all")
    iris_list = simple_file("insights_commands/iris_list")
    iscsiadm_m_session = simple_file("insights_commands/iscsiadm_-m_session")
    journal_header = simple_file("insights_commands/journalctl_--no-pager_--header")
    kpatch_list = simple_file("insights_commands/kpatch_list")
    localtime = simple_file("insights_commands/file_-L_.etc.localtime")
    losetup = simple_file("insights_commands/losetup_-l")
    lpstat_p = simple_file("insights_commands/lpstat_-p")
    ls_boot = simple_file("insights_commands/ls_-lanR_.boot")
    ls_dev = simple_file("insights_commands/ls_-lanR_.dev")
    ls_sys_firmware = simple_file("insights_commands/ls_-lanR_.sys.firmware")
    lsblk = simple_file("insights_commands/lsblk")
    lsblk_pairs = simple_file(
        "insights_commands/lsblk_-P_-o_NAME_KNAME_MAJ_MIN_FSTYPE_MOUNTPOINT_LABEL_UUID_RA_RO_RM_MODEL_SIZE_STATE_OWNER_GROUP_MODE_ALIGNMENT_MIN-IO_OPT-IO_PHY-SEC_LOG-SEC_ROTA_SCHED_RQ-SIZE_TYPE_DISC-ALN_DISC-GRAN_DISC-MAX_DISC-ZERO"
    )
    lscpu = simple_file("insights_commands/lscpu")
    lsmod = simple_file("insights_commands/lsmod")
    lsof = simple_file("insights_commands/lsof")
    lspci = simple_file("insights_commands/lspci_-k")
    lspci_vmmkn = simple_file("insights_commands/lspci_-vmmkn")
    lssap = simple_file("insights_commands/usr.sap.hostctrl.exe.lssap")
    lsscsi = simple_file("insights_commands/lsscsi")
    lvm_fullreport = simple_file(
        "insights_commands/lvm_fullreport_-a_--nolocking_--reportformat_json"
    )
    lvmconfig = first_file(
        ["insights_commands/lvmconfig_--type_full", "insights_commands/lvm_dumpconfig_--type_full"]
    )
    lvs_noheadings = first_file(
        [
            "insights_commands/lvs_--nameprefixes_--noheadings_--separator_-a_-o_lv_name_lv_size_lv_attr_mirror_log_vg_name_devices_region_size_data_percent_metadata_percent_segtype_seg_monitor_lv_kernel_major_lv_kernel_minor_--config_global_locking_type_0",
            "insights_commands/lvs_--nameprefixes_--noheadings_--separator_-a_-o_lv_name_lv_size_lv_attr_mirror_log_vg_name_devices_region_size_data_percent_metadata_percent_segtype_seg_monitor_--config_global_locking_type_0",
        ]
    )
    max_uid = simple_file("insights_commands/awk_-F_if_3_max_max_3_END_print_max_.etc.passwd")
    md5chk_files = glob_file("insights_commands/md5sum_*")
    mdadm_D = simple_file("insights_commands/mdadm_-D_.dev.md")
    mount = simple_file("insights_commands/mount")
    mokutil_sbstate = simple_file("insights_commands/mokutil_--sb-state")
    multicast_querier = simple_file(
        "insights_commands/find_.sys.devices.virtual.net._-name_multicast_querier_-print_-exec_cat"
    )
    multipath_conf_initramfs = simple_file("insights_commands/lsinitrd_-f_.etc.multipath.conf")
    multipath__v4__ll = simple_file("insights_commands/multipath_-v4_-ll")
    mysqladmin_vars = simple_file("insights_commands/mysqladmin_variables")
    named_checkconf_p = simple_file("insights_commands/named-checkconf_-p")
    ndctl_list_Ni = simple_file("insights_commands/ndctl_list_-Ni")
    netstat = simple_file("insights_commands/netstat_-neopa")
    netstat_i = simple_file("insights_commands/netstat_-i")
    netstat_s = simple_file("insights_commands/netstat_-s")
    nmap_ssh = simple_file("insights_commands/nmap_--script_ssh2-enum-algos_-sV_-p_22_127.0.0.1")
    nmcli_conn_show = simple_file("insights_commands/nmcli_conn_show")
    nmcli_dev_show = simple_file("insights_commands/nmcli_dev_show")
    ntpq_pn = simple_file("insights_commands/ntpq_-pn")
    numeric_user_group_name = simple_file("insights_commands/grep_-c_digit_.etc.passwd_.etc.group")
    nvidia_smi_l = simple_file("insights_commands/nvidia-smi_-L")
    od_cpu_dma_latency = simple_file("insights_commands/od_-An_-t_d_.dev.cpu_dma_latency")
    ovs_vsctl_list_bridge = simple_file("insights_commands/ovs-vsctl_list_bridge")
    ovs_vsctl_show = simple_file("insights_commands/ovs-vsctl_show")
    package_provides_command = glob_file("insights_commands/echo_*java*")
    parted__l = simple_file("insights_commands/parted_-l_-s")
    pci_rport_target_disk_paths = simple_file(
        "insights_commands/find_.sys.devices._-maxdepth_10_-mindepth_9_-name_stat_-type_f"
    )
    pcp_metrics = simple_file(
        "insights_commands/curl_-s_http_..127.0.0.1_44322.metrics_--connect-timeout_5"
    )
    pcs_quorum_status = simple_file("insights_commands/pcs_quorum_status")
    pcs_status = simple_file("insights_commands/pcs_status")
    pidstat = simple_file("insights_commands/pidstat")
    pmrep_metrics = first_file(
        [
            "insights_commands/pmrep_-t_1s_-T_1s_network.interface.out.packets_network.interface.collisions_swap.pagesout_mssql.memory_manager.stolen_server_memory_mssql.memory_manager.total_server_memory_-o_csv",
            "insights_commands/pmrep_-t_1s_-T_1s_network.interface.out.packets_network.interface.collisions_swap.pagesout_-o_csv",
        ]
    )
    podman_list_containers = simple_file("insights_commands/podman_ps_--all_--no-trunc")
    postconf_builtin = simple_file("insights_commands/postconf_-C_builtin")
    postconf = simple_file("insights_commands/postconf")
    ps_alxwww = simple_file("insights_commands/ps_alxwww")
    ps_aux = simple_file("insights_commands/ps_aux")
    ps_auxcww = simple_file("insights_commands/ps_auxcww")
    ps_auxww = simple_file("insights_commands/ps_auxww")
    ps_ef = simple_file("insights_commands/ps_-ef")
    ps_eo = first_file(
        ["insights_commands/ps_-eo_pid_ppid_comm_nlwp", "insights_commands/ps_-eo_pid_ppid_comm"]
    )
    puppet_ca_cert_expire_date = simple_file(
        "insights_commands/openssl_x509_-in_.etc.puppetlabs.puppet.ssl.ca.ca_crt.pem_-enddate_-noout"
    )
    pvs_noheadings = simple_file(
        "insights_commands/pvs_--nameprefixes_--noheadings_--separator_-a_-o_pv_all_vg_name_--config_global_locking_type_0"
    )
    readlink_e_etc_mtab = simple_file("insights_commands/readlink_-e_.etc.mtab")
    readlink_e_shift_cert_client = simple_file(
        "insights_commands/readlink_-e_.etc.origin.node.certificates.kubelet-client-current.pem"
    )
    readlink_e_shift_cert_server = simple_file(
        "insights_commands/readlink_-e_.etc.origin.node.certificates.kubelet-server-current.pem"
    )
    repquota_agnpuv = simple_file("insights_commands/repquota_-agnpuv")
    rhsm_katello_default_ca_cert = simple_file(
        "insights_commands/openssl_x509_-in_.etc.rhsm.ca.katello-default-ca.pem_-noout_-issuer"
    )
    rndc_status = simple_file("insights_commands/rndc_status")
    rpm_ostree_status = simple_file("insights_commands/rpm-ostree_status_--json")
    saphostctl_getcimobject_sapinstance = simple_file(
        "insights_commands/usr.sap.hostctrl.exe.saphostctrl_-function_GetCIMObject_-enuminstances_SAPInstance"
    )
    satellite_content_hosts_count = first_file(
        [
            "insights_commands/sudo_-iu_postgres_.usr.bin.psql_-d_foreman_-c_select_count_from_hosts",
            "insights_commands/sudo_-iu_postgres_psql_-d_foreman_-c_select_count_from_hosts",
        ]
    )
    satellite_custom_ca_chain = simple_file(
        "insights_commands/awk_BEGIN_pipe_openssl_x509_-noout_-subject_-enddate_._-_BEGIN_CERT._._-_END_CERT._print_pipe_._-_END_CERT._close_pipe_printf_n_.etc.pki.katello.certs.katello-server-ca.crt"
    )
    satellite_provision_param_settings = simple_file(
        'insights_commands/sudo_-iu_postgres_.usr.bin.psql_-d_foreman_-c_select_name_value_from_parameters_where_name_package_upgrade_and_reference_id_in_select_id_from_operatingsystems_where_name_RedHat_and_major_9_--csv'
    )
    satellite_qualified_capsules = simple_file(
        "insights_commands/sudo_-iu_postgres_.usr.bin.psql_-d_foreman_-c_select_name_from_smart_proxies_where_download_policy_background_--csv"
    )
    satellite_qualified_katello_repos = simple_file(
        "insights_commands/sudo_-iu_postgres_.usr.bin.psql_-d_foreman_-c_select_id_name_url_download_policy_from_katello_root_repositories_where_download_policy_background_or_url_is_NULL_--csv"
    )
    sealert = simple_file('insights_commands/sealert_-l')
    sestatus = simple_file("insights_commands/sestatus_-b")
    smbstatus_p = simple_file("insights_commands/smbstatus_-p")
    software_collections_list = simple_file('insights_commands/scl_--list')
    spamassassin_channels = simple_file(
        'insights_commands/grep_-r_s_CHANNELURL_.etc.mail.spamassassin.channel.d'
    )
    ss = simple_file("insights_commands/ss_-tupna")
    sshd_config_perms = first_file(
        [
            "insights_commands/ls_-lH_.etc.ssh.sshd_config",
            "insights_commands/ls_-l_.etc.ssh.sshd_config",
        ]
    )
    subscription_manager_facts = simple_file("insights_commands/subscription-manager_facts")
    subscription_manager_id = simple_file("insights_commands/subscription-manager_identity")
    subscription_manager_installed_product_ids = simple_file(
        "insights_commands/find_.etc.pki.product-default._.etc.pki.product._-name_pem_-exec_rct_cat-cert_--no-content"
    )
    subscription_manager_status = simple_file("insights_commands/subscription-manager_status")
    sysctl = simple_file("insights_commands/sysctl_-a")
    systemctl_cat_rpcbind_socket = simple_file("insights_commands/systemctl_cat_rpcbind.socket")
    systemctl_get_default = simple_file("insights_commands/systemctl_get-default")
    systemctl_list_unit_files = simple_file("insights_commands/systemctl_list-unit-files")
    systemctl_list_units = simple_file("insights_commands/systemctl_list-units")
    systemctl_show_all_services = simple_file("insights_commands/systemctl_show_.service")
    systemctl_show_target = simple_file("insights_commands/systemctl_show_.target")
    systemd_analyze_blame = simple_file("insights_commands/systemd-analyze_blame")
    systemd_docker = first_file(
        ["insights_commands/systemctl_cat_docker.service", "/usr/lib/systemd/system/docker.service"]
    )
    systemd_openshift_node = first_file(
        [
            "insights_commands/systemctl_cat_atomic-openshift-node.service",
            "/usr/lib/systemd/system/atomic-openshift-node.service",
        ]
    )
    testparm_s = simple_file("insights_commands/testparm_-s")
    testparm_v_s = simple_file("insights_commands/testparm_-v_-s")
    timedatectl_status = simple_file("insights_commands/timedatectl_status")
    tomcat_vdc_fallback = simple_file(
        "insights_commands/find_.usr.share_-maxdepth_1_-name_tomcat_-exec_.bin.grep_-R_-s_VirtualDirContext_--include_.xml"
    )
    tuned_adm = simple_file("insights_commands/tuned-adm_list")
    uname = simple_file("insights_commands/uname_-a")
    uptime = simple_file("insights_commands/uptime")
    vdo_status = simple_file("insights_commands/vdo_status")
    vgdisplay = simple_file("insights_commands/vgdisplay")
    vgs_noheadings = simple_file(
        "insights_commands/vgs_--nameprefixes_--noheadings_--separator_-a_-o_vg_all_--config_global_locking_type_0"
    )
    virsh_list_all = simple_file("insights_commands/virsh_--readonly_list_--all")
    virt_what = simple_file("insights_commands/virt-what")
    wc_proc_1_mountinfo = simple_file("insights_commands/wc_-l_.proc.1.mountinfo")
    xfs_quota_state = simple_file("insights_commands/xfs_quota_-x_-c_state_-gu")
    yum_list_available = simple_file("insights_commands/yum_-C_--noplugins_list_available")
    yum_repolist = first_file(
        [
            "insights_commands/yum_-d_2_-C_--noplugins_repolist",
            "insights_commands/yum_-C_--noplugins_repolist",
            "insights_commands/yum_-C_repolist",
        ]
    )
    yum_updateinfo = simple_file("insights_commands/yum_-C_updateinfo_list")
