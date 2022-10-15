Name:		eekboard
Version:	1.0.8
Release:	6
Summary:	Yet Another Virtual Keyboard

Group:		System/X11
License:	GPLv3+
URL:		http://fedorahosted.org/eekboard/
Source0:	https://github.com/ueno/eekboard/archive/refs/tags/eekboard-%{version}.tar.gz
Patch0:		eekboard-stop-key-repeat.patch
BuildRequires:	gnome-common, gettext-devel
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(atspi-2)
BuildRequires:	intltool desktop-file-utils
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libcroco-0.6)
BuildRequires:	vala-tools

Requires:	eekboard-service = %{version}-%{release}
Provides:	eekboard-python = %{version}-%{release}
Obsoletes:	eekboard-python < 1.0.5-5

%description
eekboard is a virtual keyboard software package, including a set of
tools to implement desktop virtual keyboards.

%package service
Summary:	Runtime service for eekboard
Group:		System/X11

Requires:	%{name}-libs = %{version}-%{release}

%description service
This package contains the D-Bus service for eekboard

%package libs
Summary:	Runtime libraries for eekboard
Group:		System/Libraries
License:	LGPLv2+

%description libs
This package contains the libraries for eekboard

%package devel
Summary:	Development tools for eekboard
Group:		Development/X11
License:	LGPLv2+ and GFDL

Requires:	vala
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the development tools for eekboard.


%prep
%setup -q
%patch0 -p1 -b .stop-key-repeat

AUTOPOINT='intltoolize --automake --copy' autoreconf -fi


%build
%configure --disable-static --enable-atspi
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

# We don't install autostart file to avoid conflict with other OSK.
# Instead, install it under doc.
mkdir -p base-installed/examples
mv $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop base-installed/examples

desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans libs
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/sbin/ldconfig


%files -f %{name}.lang
%doc base-installed/examples
%{_bindir}/eekboard
%{_libexecdir}/eekboard-setup
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/eekboard.png
%{_datadir}/icons/hicolor/scalable/apps/eekboard.svg

%files service
%{_bindir}/eekboard-server
%{_datadir}/dbus-1/services/eekboard-server.service
%{_datadir}/eekboard/
%{_datadir}/glib-2.0/schemas/*

%files libs
%doc AUTHORS COPYING README
%{_libdir}/libeek*.so.*
%{_libdir}/girepository-1.0/Eek*.typelib

%files devel
# LGPLv2+
%{_libdir}/libeek*.so
%{_includedir}/eek-0.90/
%{_includedir}/eekboard-0.90/
%{_datadir}/gir-1.0/Eek*.gir
%{_datadir}/vala/vapi/eek*.vapi
%{_datadir}/vala/vapi/eek*.deps
%{_libdir}/pkgconfig/eek*.pc
# GFDL
%{_datadir}/gtk-doc/html/*


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  2 2013 Daiki Ueno <dueno@redhat.com> - 1.0.8-4
- pull the latest config.guess and config.sub for ARM64 support

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct  5 2012 Daiki Ueno <dueno@redhat.com> - 1.0.8-2
- add eekboard-stop-key-repeat.patch (#857977)

* Wed Aug 15 2012 Daiki Ueno <dueno@redhat.com> - 1.0.8-1
- split eekboard-server into eekboard-service package (fixes #847500)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Daiki Ueno <dueno@redhat.com> - 1.0.7-2
- remove unnecessary BR: dbus-glib-devel
- add eekboard-fix-crash.patch

* Fri Apr 13 2012 Daiki Ueno <dueno@redhat.com> - 1.0.7-1
- new upstream release
- drop unnecessary %%defattr(-,root,root,-) from %%files

* Sat Mar 31 2012 Daiki Ueno <dueno@redhat.com> - 1.0.6-2
- add provides/obsoletes for -python subpackage (fixes #808634)

* Fri Mar 30 2012 Daiki Ueno <dueno@redhat.com> - 1.0.6-1
- new upstream release
- drop IBus dependency
- drop Python binding

* Tue Mar  6 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.5-4
- Rebuild for ibus 1.4.99.20120304

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Daiki Ueno <dueno@redhat.com> - 1.0.5-2
- drop gir-repository-devel from conditional BR

* Fri Nov 25 2011 Daiki Ueno <dueno@redhat.com> - 1.0.5-1
- new upstream release (fixes #739330, #756909)

* Fri Sep 30 2011 Daiki Ueno <dueno@redhat.com> - 1.0.4-1
- new upstream release (fixes #737441)

* Thu Sep 29 2011 Daiki Ueno <dueno@redhat.com> - 1.0.3-5
- add eekboard-command-line-keyboards.patch (#737441)

* Mon Sep 12 2011 Daiki Ueno <dueno@redhat.com> - 1.0.3-4
- fix eekboard-send-key-event-for-text.patch (#737440)

* Mon Sep 12 2011 Daiki Ueno <dueno@redhat.com> - 1.0.3-3
- add eekboard-send-key-event-for-text.patch

* Mon Sep 12 2011 Daiki Ueno <dueno@redhat.com> - 1.0.3-2
- add eekboard-window-size-constraint.patch
- add eekboard-fix-key-release-race-condition.patch (#737396)

* Thu Sep  1 2011 Daiki Ueno <dueno@redhat.com> - 1.0.3-1
- new upstream release

* Fri Aug 26 2011 Daiki Ueno <dueno@redhat.com> - 1.0.2-3
- install eekboard-autostart.desktop under %%doc/examples instead of
  the autostart dir to avoid conflict with other at-spi based OSK
- install simple-client under %%doc/examples
- remove unnecessary dependency on python-virtkey
- add eekboard-python-binding-fix.patch

* Thu Aug 25 2011 Daiki Ueno <dueno@redhat.com> - 1.0.2-1
- new upstream release

* Mon Aug 15 2011 Daiki Ueno <dueno@redhat.com> - 1.0.1-2
- add eekboard-key-repeat.patch

* Mon Aug 15 2011 Daiki Ueno <dueno@redhat.com> - 1.0.1-1
- new upstream release

* Fri Aug 12 2011 Daiki Ueno <dueno@redhat.com> - 1.0.0-1
- new upstream release

* Thu May 26 2011 Daiki Ueno <dueno@redhat.com> - 0.90.7-2
- remove runtime dependency on gtk-doc (#707551)
- let the base package depend on eekboard-python instead of
  eekboard-libs, for eekboard-inscript

* Fri Apr 22 2011 Daiki Ueno <dueno@redhat.com> - 0.90.7-1
- new upstream release
- link against at-spi2-core
- install eekboard-autostart.desktop

* Tue Apr 19 2011 Daiki Ueno <dueno@redhat.com> - 0.90.6-3
- don't link against CSPI-1.0 (fixes #697546)

* Fri Apr 15 2011 Daiki Ueno <dueno@redhat.com> - 0.90.6-2
- apply a patch to fix Exec in desktop file

* Fri Mar 11 2011 Daiki Ueno <dueno@redhat.com> - 0.90.6-1
- new upstream release

* Fri Mar 11 2011 Daiki Ueno <dueno@redhat.com> - 0.90.5-2
- apply a patch to support newer pygobject2

* Fri Mar 11 2011 Daiki Ueno <dueno@redhat.com> - 0.90.5-1
- new upstream release

* Tue Mar  8 2011 Daiki Ueno <dueno@redhat.com> - 0.90.4-2
- add eekboard-annotation.patch needed by newer pygobject2

* Tue Mar  8 2011 Daiki Ueno <dueno@redhat.com> - 0.90.4-1
- new upstream release

* Wed Mar  2 2011 Daiki Ueno <dueno@redhat.com> - 0.90.3-1
- new upstream release (fixes #680406 and 680826)

* Thu Feb 24 2011 Daiki Ueno <dueno@redhat.com> - 0.90.2-1
- new upstream release

* Wed Feb 23 2011 Daiki Ueno <dueno@redhat.com> - 0.90.1-1
- new upstream release

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 0.0.7-7
- Rebuild against newer libxklavier

* Fri Feb 11 2011 Matthias Clasen <mclasne@redhat.com> - 0.0.7-6
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.7-4
- Rebuild against newer gtk3

* Thu Jan 13 2011 Daiki Ueno <dueno@redhat.com> - 0.0.7-3
- add eekboard-gtk3.patch

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.7-2
- Rebuild against newer gtk3

* Mon Dec  6 2010 Daiki Ueno <dueno@redhat.com> - 0.0.7-1
- new upstream release

* Mon Nov 15 2010 Daiki Ueno <dueno@redhat.com> - 0.0.6-1
- new upstream release
- remove patches for GTK3 and libnotify since they are included in the
  upstream
- enable clutter build again

* Fri Nov 12 2010 Daiki Ueno <dueno@redhat.com> - 0.0.5-4
- apply patch to fix build against GTK 2.91.5
- apply patch to fix build against libnotify 0.7.0
- temporarily disable clutter since clutter-gtk uses GTK2 symbols

* Wed Sep  8 2010 Daiki Ueno <dueno@redhat.com> - 0.0.5-3
- link against gtk+-3.0 since clutter-gtk-1.0 requires it

* Tue Sep  7 2010 Daiki Ueno <dueno@redhat.com> - 0.0.5-2
- rebuild to resolve broken dependency on clutter-gtk

* Thu Aug 12 2010 Daiki Ueno <dueno@redhat.com> - 0.0.5-1
- new upstream release
- remove disable Clutter patch
- add a shell script wrapper for eekboard to disable Clutter

* Wed Jul 14 2010 Daiki Ueno <dueno@redhat.com> - 0.0.4-2
- apply a patch to disable Clutter by default (#611888)

* Thu Jul  1 2010 Daiki Ueno <dueno@redhat.com> - 0.0.4-1
- new upstream release
- merge -devel-docs to -devel

* Tue Jun 29 2010 Daiki Ueno <dueno@redhat.com> - 0.0.3-5
- pass "-p" to the install command called on "make install"
- fix directory ownership of %%{_includedir}/eek-1.0/

* Mon Jun 28 2010 Daiki Ueno <dueno@redhat.com> - 0.0.3-4
- don't add gir-repository-devel to BR when building on F-13 or earlier

* Mon Jun 28 2010 Daiki Ueno <dueno@redhat.com> - 0.0.3-3
- reduced the number of BR using dependency
- add gir-repository-devel to BR
- make eekboard-devel depend on vala
- fix directory ownership of %%{_includedir}/eek-1.0/eek/

* Thu Jun 24 2010 Daiki Ueno <dueno@redhat.com> - 0.0.3-2
- add libXtst-devel to BR

* Wed Jun 23 2010 Daiki Ueno <dueno@redhat.com> - 0.0.3-1
- new upstream release

* Wed Jun 23 2010 Daiki Ueno <dueno@redhat.com> - 0.0.2-2
- rename subpackages from libeek* to eekboard-libs*
- reduce the number of subpackages

* Tue Jun 22 2010 Daiki Ueno <dueno@redhat.com> - 0.0.2-1
- initial packaging for Fedora
