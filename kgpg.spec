Name:    kgpg
Summary: Manage GPG encryption keys 
Version: 4.10.5
Release: 2%{?dist}

License: GPLv2+
#URL:     https://projects.kde.org/projects/kde/kdeutils/%{name}
URL:     http://utils.kde.org/projects/%{name}
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstreamable patches
# add support for gpg2 to kgpg 
Patch50: kgpg-4.8.80-gpg2.patch

# Upstream patches
# Fix #997594 - misbehaving checkbox "Allow encryption with untrusted keys"
Patch100: kgpg-4.10-RHBZ997594.patch

# Upstreamed patches
# Fix #997599 - Key Manager does not refresh after change
Patch200: kgpg-4.10-RHBZ997599.patch
# Fix #999850 - kgpg shows error message despite the change was successful
Patch201: kgpg-4.10-RHBZ999850.patch

BuildRequires: desktop-file-utils
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}

# when split occured
Conflicts: kdeutils-common < 6:4.7.80

Obsoletes: kdeutils-kgpg < 6:4.7.80
Provides:  kdeutils-kgpg = 6:%{version}-%{release}

%{?_kde4:Requires: kdepimlibs%{?_isa} >= %{_kde4_version}}
# kgpg (can be either gnupg or gnupg2, we'll default to the latter)
Requires: gnupg2


%description
KGpg is a simple interface for GnuPG, a powerful encryption utility.

%prep
%setup -q -n %{name}-%{version}

%patch50 -p1 -b .gpg2
%patch100 -p1 -b .rhbz997594
%patch200 -p1 -b .rhbz997599
%patch201 -p1 -b .rhbz999850

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde --without-mo


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/%{name}.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:
fi

%files -f %{name}.lang
%doc AUTHORS COPYING
%{_kde4_bindir}/kgpg
%{_kde4_appsdir}/kgpg/
%{_datadir}/dbus-1/interfaces/org.kde.kgpg.*.xml
%{_kde4_datadir}/config.kcfg/kgpg.kcfg
%{_kde4_datadir}/autostart/kgpg.desktop
%{_kde4_iconsdir}/hicolor/*/apps/kgpg.*
%{_kde4_datadir}/applications/kde4/kgpg.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/encryptfile.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/encryptfolder.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/viewdecrypted.desktop



%changelog
* Tue Oct 01 2013 Daniel Vrátil <dvratil@redhat.com> - 4.10.5-2
- Resolves: #997594, misbehaving checkbox "Allow encryption with untrusted keys"
- Resolves: #997599, Key Manager does not refresh after change
- Resolves: #999850, shows error message despite the change was successful 

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Mon Apr 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.95-1
- 4.8.95

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Sun Jun 03 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Tue Jan 24 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.0-2
- respin

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.7.97-1
- 4.7.97

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Thu Dec 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Tue Nov 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-2
- improve Summary
- fix Source0 url

* Sat Nov 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- first try

