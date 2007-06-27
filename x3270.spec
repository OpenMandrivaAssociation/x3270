%define	tversion	3.3
%define icumaj		36

Summary:	An X Window System based IBM 3278/3279 terminal emulator
Name:		x3270
Version:	3.3.6
Release:	%mkrel 1
License:	MIT
Group:		Terminals
URL:		http://www.geocities.com/SiliconValley/Peaks/7814/
Source:		http://prdownloads.sourceforge.net/x3270/x3270-%{version}.tar.bz2

Requires(pre):	xorg-x11
Requires(post):	xorg-x11
BuildRequires:	imake rman bdftopcf
BuildRequires:	icu%{icumaj}-devel openssl-devel 
BuildRequires:	X11-devel dos2unix icu
BuildRequires:	x11-data-bitmaps
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
#export PROJECTROOT=%{_prefix}
%configure	--enable-ssl \
		--with-fontdir=%{_datadir}/fonts/misc

%make PROJECTROOT=%{_prefix}
# (sb) hack to get around ProjectRoot that insists on 
# getting picked up from broken site.def
#rm -f *.gz
#%make

%install
rm -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=X3270
Comment=IBM 3270 Terminal Emulator
Exec=%{_bindir}/x3270
Icon=terminals_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=TerminalEmulator;X-MandrivaLinux-System-Terminals;
EOF

# (sb) hack to get around ProjectRoot that insists on 
# getting picked up from broken site.def
sed -i 's|X11R6/bin|bin|' Makefile
sed -i 's|/usr/X11R6/man|%{_mandir}|' Makefile

%makeinstall_std install.man PROJECTROOT=%{_prefix} MANPATH=%{_mandir}

install -m644 X3270.xad -D %{buildroot}%{_sysconfdir}/X11/app-defaults/X3270

rm -f %buildroot%{_datadir}/fonts/misc/fonts.dir

# David - 3.2.14 - Workaround to don't requires stuff in /usr/local
# (sb) tradeoff rpmlint doesn't like non-executable scripts, but
# I'd rather not require expect and ksh
chmod 0644 Examples/*.{expect,ksh}
chmod 0755 Examples/*.{sh,bash}

# (sb) make rpmlint happier
chmod 0644 html/*.html
dos2unix -U -f html/Brackets.html
dos2unix -U -f html/Build.html
dos2unix -U -f html/Keymap.html
sed -i 's|usr/local|usr|g' Examples/peer_script.expect
sed -i 's|usr/local|usr|g' Examples/cms_logon.bash
chmod -x %buildroot%{_sysconfdir}/%{name}/*

# (sb) old /usr/X11R6/lib/doc/html seems to be gone now - just catch this with %doc
rm -fr %buildroot%{_prefix}/X11R6/lib/X11/doc

%clean
rm -rf %{buildroot}

%post
mkfontdir %{_datadir}/fonts/misc
%update_menus

%postun
mkfontdir %{_datadir}/fonts/misc
%clean_menus

%files
%defattr(-,root,root)
%doc Examples html
%{_bindir}/%{name}
%{_bindir}/pr3287
%{_bindir}/x3270if
%{_datadir}/fonts/misc/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_datadir}/applications/%{name}.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
