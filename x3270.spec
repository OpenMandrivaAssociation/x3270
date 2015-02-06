%define	tversion	3.3

Summary:	An X Window System based IBM 3278/3279 terminal emulator
Name:		x3270
Version:	3.3.9ga12
Release:	5
License:	MIT
Group:		Terminals
URL:		http://www.geocities.com/SiliconValley/Peaks/7814/
Source0:	http://downloads.sourceforge.net/project/x3270/x3270/%version/suite3270-%version.tgz

Requires(post):		mkfontdir
Requires(postun):	mkfontdir

BuildRequires:	bdftopcf
BuildRequires:	dos2unix
#BuildRequires:	mkfontdir
#BuildRequires:	mkfontscale
BuildRequires:	imake
BuildRequires:	openssl-devel 
#BuildRequires:	rman
#BuildRequires:	x11-data-bitmaps
BuildRequires:  pkgconfig(x11)
BuildRequires:  xaw-devel
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xt)

%description
The x3270 program opens a window in the X Window System which emulates
the actual look of an IBM 3278/3279 terminal, commonly used with
mainframe applications. x3270 also allows you to telnet to an IBM host
from the x3270 window.

Install the x3270 package if you need to access IBM hosts using an
IBM 3278/3279 terminal emulator.

%prep
%setup -q -n %{name}-%{tversion}

%build
%configure2_5x	--enable-ssl \
		--with-fontdir=%{_datadir}/fonts/misc

%make PROJECTROOT=%{_prefix}
# (sb) hack to get around ProjectRoot that insists on 
# getting picked up from broken site.def
#rm -f *.gz
#%make

%install
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=X3270
Comment=IBM 3270 Terminal Emulator
Exec=%{_bindir}/x3270
Icon=terminals_section
Terminal=false
Type=Application
StartupNotify=true
Categories=TerminalEmulator;System;
EOF

# (sb) hack to get around ProjectRoot that insists on 
# getting picked up from broken site.def
sed -i 's|X11R6/bin|bin|' Makefile
sed -i 's|/usr/X11R6/man|%{_mandir}|' Makefile

%makeinstall_std install.man PROJECTROOT=%{_prefix} MANPATH=%{_mandir}

install -m644 X3270.xad -D %{buildroot}%{_sysconfdir}/X11/app-defaults/X3270

rm -f %{buildroot}%{_datadir}/fonts/misc/fonts.dir

# David - 3.2.14 - Workaround to don't requires stuff in /usr/local
# (sb) tradeoff rpmlint doesn't like non-executable scripts, but
# I'd rather not require expect and ksh
chmod 0644 Examples/*.{expect,ksh}
chmod 0755 Examples/*.{sh,bash}

# (sb) make rpmlint happier
chmod 0644 html/*.html
dos2unix -f html/Brackets.html
dos2unix -f html/Build.html
dos2unix -f html/Keymap.html
sed -i 's|usr/local|usr|g' Examples/peer_script.expect
sed -i 's|usr/local|usr|g' Examples/cms_logon.bash
chmod -x %buildroot%{_sysconfdir}/%{name}/*

# (sb) old /usr/X11R6/lib/doc/html seems to be gone now - just catch this with %doc
rm -fr %buildroot%{_prefix}/X11R6/lib/X11/doc

%post
mkfontdir %{_datadir}/fonts/misc

%postun
mkfontdir %{_datadir}/fonts/misc

%files
%defattr(-,root,root)
%doc Examples html
%{_bindir}/*
%{_datadir}/fonts/misc/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/applications/%{name}.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3.9ga12-3mdv2011.0
+ Revision: 615488
- the mass rebuild of 2010.1 packages

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 3.3.9ga12-2mdv2010.1
+ Revision: 533618
- rebuild

* Wed Aug 12 2009 Funda Wang <fwang@mandriva.org> 3.3.9ga12-1mdv2010.0
+ Revision: 415322
- new version 3.3.9ga12

* Sat Mar 28 2009 Funda Wang <fwang@mandriva.org> 3.3.8p1-2mdv2009.1
+ Revision: 362017
- rebuild

* Thu Dec 04 2008 Adam Williamson <awilliamson@mandriva.org> 3.3.8p1-1mdv2009.1
+ Revision: 309851
- clean some unnecessary dependencies
- new release 3.3.8p1

* Sat Sep 20 2008 Oden Eriksson <oeriksson@mandriva.com> 3.3.6-7mdv2009.0
+ Revision: 286226
- fix deps

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Nov 26 2007 Funda Wang <fwang@mandriva.org> 3.3.6-3mdv2008.1
+ Revision: 112163
- rebuild for new icu

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild for new libicu
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Wed Jun 27 2007 Funda Wang <fwang@mandriva.org> 3.3.6-1mdv2008.0
+ Revision: 44958
- BuildRequires bitmaps
- fix file list
- New version

  + Jérôme Soyer <saispo@mandriva.org>
    - Import x3270



* Wed Aug 23 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 3.3.4p6-4mdv2007.0
- adapt to new font path
- fix path for man page x3270.1x
- cosmetics

* Thu Jul 06 2006 Stew Benedict <sbenedict@mandriva.com> 3.3.4p6-3mdv2007.0
- bug #22937 (fonts -> /usr/lib/X11/fonts/misc)
- would be nice if site.def defined a different ProjectRoot than /usr/X11R6
- tweak the rest of the paths for the new X layout
- rpmlint fixes, xdg menu

* Mon Jan 30 2006 Stew Benedict <sbenedict@mandriva.com> 3.3.4p6-2mdk
- more BuildRequires

* Mon Jan 30 2006 Stew Benedict <sbenedict@mandriva.com> 3.3.4p6-1mdk
- 3.3.4p6, BuildRequires, rpmlint

* Fri Jan 27 2006 Stew Benedict <sbenedict@mandriva.com> 3.3.4-4mdk
- rebuild against icu34-devel
- Requires(pre/post)

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.4-3mdk
- rebuilt against openssl-0.9.8a

* Tue May 10 2005 Arnaud de Lorbeau <devel@mandriva.com> 3.3.4-2mdk
- 3.3.4

* Thu Jul 22 2004 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 3.3.2p1-2mdk
- Rebuild with ssl

* Mon May  3 2004 Stew Benedict <sbenedict@mandrakesoft.com> 3.3.2p1-1mdk
- 3.3.2p1, patch to build with current icu

* Mon Apr 28 2003 Stew Benedict <sbenedict@mandrakesoft.com> 3.2.20-1mdk
- 3.2.20, BuildRequires, spec-work

* Mon Jan  6 2003 Stew Benedict <sbenedict@mandrakesoft.com> 3.2.19-2mdk
- rebuild for new glibc/rpm, rpmlint fixes

* Wed May 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 3.2.19-1mdk
- new version
- misc spec file fixes
- rebuilt with latest system compiler (gcc3.1)

* Thu Jan 10 2002 David BAUDENS <baudens@mandrakesoft.com> 3.2.17-4mdk
- Fix menu entry (png icon)
- Add missing files

* Thu Aug 23 2001 David BAUDENS <baudens@mandrakesoft.com> 3.2.17-3mdk
- Move menu entry in right directory

* Tue Jul 10 2001 Stefan van der Eijk <stefan@eijk.nu> 3.2.17-2mdk
- BuildRequires: XFree86-devel

* Mon Jul 9 2001 Gregory Letoquart <gletoquart@mandrakesoft.com> 3.2.17-1mdk
- 3.2.17

* Thu Dec 27 2000 Gregory Letoquart <gletoquart@mandrakesoft.com> 3.2.15-2mdk
- 3.2.15 

* Fri Nov 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.2.14-2mdk
- Workaround for ??~#* RPM

* Fri Nov 17 2000 David BAUDENS <baudens@mandrakesoft.com> 3.2.14-1mdk
- 3.2.14

* Fri Sep 29 2000 David BAUDENS <baudens@mandrakesoft.com> 3.2.13-1mdk
- 3.2.13

* Fri Sep 29 2000 David BAUDENS <baudens@mandrakesoft.com> 3.1.1.9-3mdk
- Fix conflict with XFree

* Sat Sep 09 2000 David BAUDENS <baudens@mandrakesoft.com> 3.1.1.9-2mdk
- Allow to build
- Remove wmconfig support
- BM
- %%{update_menus} && %%{clean_menus}
- Spec clean up (aka remove crazy things)
- Fix menu entry (aka remove stupid hard coded PATH for icon and fix title)

* Sat Apr 08 2000 Christopher Molnar <molnarc@mandrakesoft.com> 3.1.1.9-1mdk
- Changed group to new groups
- updated to 3.1.1.9
- added HTML docs
- Added menu to spec file

* Wed Nov 03 1999 Jerome Martin <jerome@mandrakesoft.com>
- Rebuild for new distribution
- Minor Specfile cleanup

* Thu May 06 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- ibm_hosts needed %%config (#788)

* Fri Aug  7 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 22 1997 Marc Ewing <marc@redhat.com>
- new version
- added wmconfig entry

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
