# ── Suppress debuginfo for a noarch Python script ────────────────────────────
%global debug_package %{nil}

# ─────────────────────────────────────────────────────────────────────────────
#  tuxpatch
# ─────────────────────────────────────────────────────────────────────────────
Name:           tuxpatch
Version:        %{version_string}
Release:        1%{?dist}
Summary:        RHEL workstation patch manager with TPM2/LUKS reseal support
License:        GPL-3.0-or-later
URL:            https://github.com/MrMEEE/tuxpatch
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  systemd-rpm-macros

# Runtime
Requires:       python3
Requires:       python3-pyyaml
Requires:       libnotify

# Optional but expected on managed workstations — listed as weak deps so the
# RPM installs cleanly on minimal / container images used for testing.
Recommends:     flatpak
Recommends:     dracut
Recommends:     clevis
Recommends:     clevis-luks

%description
tuxpatch is a RHEL workstation patch manager that automates:

 * DNF system upgrades (dnf upgrade --refresh)
 * Per-user and system-wide Flatpak updates (configurable)
 * Desktop notifications for users via D-Bus (configurable)
 * Automatic TPM2/LUKS reseal after RPM updates

The TPM2/LUKS reseal uses a two-boot strategy: before updating, all
Clevis bindings are relaxed to TPM-only (no PCR check) so the first
post-update boot succeeds even if PCR values changed.  A one-shot
systemd service (tuxpatch-reseal.service) then rebinds Clevis against
the fresh PCR measurements and reboots, restoring full PCR protection.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to compile — pure Python script.

%install
# ── Binary ────────────────────────────────────────────────────────────────────
install -D -m 0755 tuxpatch %{buildroot}%{_bindir}/tuxpatch

# ── Config skeleton ───────────────────────────────────────────────────────────
install -d %{buildroot}%{_sysconfdir}/tuxpatch
install -D -m 0640 config.example.yaml \
    %{buildroot}%{_sysconfdir}/tuxpatch/config

# ── State directory ───────────────────────────────────────────────────────────
install -d %{buildroot}%{_sharedstatedir}/tuxpatch

# ── Cron job (disabled by default) ───────────────────────────────────────────
install -D -m 0644 packaging/tuxpatch.cron \
    %{buildroot}%{_sysconfdir}/cron.d/tuxpatch

# ── Desktop entry (notification identity for KDE/GNOME history) ────────────
install -D -m 0644 packaging/tuxpatch.desktop \
    %{buildroot}%{_datadir}/applications/tuxpatch.desktop

# ── Systemd service (installed but not enabled by default) ─────────────────
install -D -m 0644 packaging/tuxpatch-reseal.service \
    %{buildroot}%{_unitdir}/tuxpatch-reseal.service

%files
%license LICENSE
%{_bindir}/tuxpatch
%dir %{_sysconfdir}/tuxpatch
%config(noreplace) %{_sysconfdir}/tuxpatch/config
%dir %attr(0700, root, root) %{_sharedstatedir}/tuxpatch
%config(noreplace) %{_sysconfdir}/cron.d/tuxpatch
%{_datadir}/applications/tuxpatch.desktop
%{_unitdir}/tuxpatch-reseal.service

%post
%systemd_post tuxpatch-reseal.service
# Enable on fresh install. The ConditionPathExists guard in the unit means it
# is a no-op at boot unless tuxpatch has armed it by creating the state file.
if [ $1 -eq 1 ]; then
    systemctl enable tuxpatch-reseal.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun tuxpatch-reseal.service

%postun
%systemd_postun tuxpatch-reseal.service

%changelog

* Fri Apr 17 2026 Release Bot <release@tuxpatch> - 1.0.11-1
- Release 1.0.11

* Fri Apr 17 2026 Release Bot <release@tuxpatch> - 1.0.10-1
- Release 1.0.10

* Fri Apr 17 2026 Release Bot <release@tuxpatch> - 1.0.9-1
- Release 1.0.9

* Fri Apr 17 2026 Release Bot <release@tuxpatch> - 1.0.8-1
- Release 1.0.8

* Thu Apr 16 2026 Release Bot <release@tuxpatch> - 1.0.7-1
- Release 1.0.7

* Tue Apr 14 2026 Release Bot <release@tuxpatch> - 1.0.6-1
- Release 1.0.6

* Tue Apr 14 2026 Release Bot <release@tuxpatch> - 1.0.5-1
- Release 1.0.5

* Mon Apr 13 2026 Release Bot <release@tuxpatch> - 1.0.4-1
- Release 1.0.4

* Mon Apr 06 2026 Release Bot <release@tuxpatch> - 1.0.3-1
- Release 1.0.3

* Mon Apr 06 2026 Release Bot <release@tuxpatch> - 1.0.2-1
- Release 1.0.2

* Mon Apr 06 2026 Release Bot <release@tuxpatch> - 1.0.1-1
- Release 1.0.1
