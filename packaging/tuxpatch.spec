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

# Runtime
Requires:       python3
Requires:       python3-pyyaml

# Optional but expected on managed workstations — listed as weak deps so the
# RPM installs cleanly on minimal / container images used for testing.
Recommends:     flatpak
Recommends:     dracut
Recommends:     clevis
Recommends:     clevis-luks

%description
tuxpatch is a RHEL workstation patch manager that automates:

 * DNF system upgrades (dnf upgrade --refresh)
 * Per-user and system-wide Flatpak updates
 * Automatic TPM2/LUKS reseal after kernel or shim updates

When a kernel or shim update is detected, tuxpatch builds a temporary
initrd that embeds the LUKS passphrase, creates a one-shot systemd
reseal service, then reboots into that initrd to rebind Clevis/TPM2
slots with the new PCR values before returning to normal boot.

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
    %{buildroot}%{_sysconfdir}/tuxpatch/config.yaml

# ── State directory ───────────────────────────────────────────────────────────
install -d %{buildroot}%{_sharedstatedir}/tuxpatch

%files
%license LICENSE
%{_bindir}/tuxpatch
%dir %{_sysconfdir}/tuxpatch
%config(noreplace) %{_sysconfdir}/tuxpatch/config.yaml
%dir %attr(0700, root, root) %{_sharedstatedir}/tuxpatch

%changelog
