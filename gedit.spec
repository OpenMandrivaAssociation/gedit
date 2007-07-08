%define build_with_python 1
Summary:		GEdit is a small but powerful text editor for GNOME
Name:			gedit
Version: 2.19.2
Release: %mkrel 2
License:		GPL
Group:			Editors 
Source0:		ftp://ftp.gnome.org/pub/GNOME/sources/gedit/%{name}-%{version}.tar.bz2
Patch: gedit-2.19.2-pkgconfig.patch
# (fc) use current locale when creating new file (Mdk bug 6887)
Patch1:			gedit-2.17.3-encoding.patch
# (fc) 2.8.1-1mdk make file selector remember last window size and directory (Fedora)
Patch4:			gedit-2.13.2-filesel.patch
URL:			http://www.gnome.org/projects/gedit/
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libgnomeprintui-devel >= 2.6.0
BuildRequires:	gtksourceview-devel >= 1.90.2
BuildRequires:	libgnomeui2-devel >= 2.16.0
BuildRequires:	gnome-vfs2-devel >= 2.16.0
BuildRequires:  aspell-devel
BuildRequires:  libattr-devel
BuildRequires:  enchant-devel
BuildRequires:  iso-codes
BuildRequires:  scrollkeeper
BuildRequires:  perl-XML-Parser
BuildRequires:  gnome-doc-utils
BuildRequires:  gtk-doc
%if %{build_with_python}
BuildRequires:  gnome-python
BuildRequires: pygtk2.0-devel >= 2.9.7
BuildRequires: python-gtksourceview-devel >= 1.90.2
BuildRequires: libglade2.0-devel
Requires: gnome-python-gnomevfs
Requires: pygtk2.0-libglade
Requires: python-gtksourceview
%endif
BuildRequires:  gtk+2-devel >= 2.5.4
BuildRequires: desktop-file-utils
Requires: pyorbit
Requires(post):		scrollkeeper >= 0.3 desktop-file-utils
Requires(postun):	scrollkeeper >= 0.3 desktop-file-utils
Conflicts:		gedit-plugins <= 2.3.2-1mdk

%description
gEdit is a small but powerful text editor designed expressly
for GNOME.

It includes such features as split-screen mode, a plugin
API, which allows gEdit to be extended to support many
features while remaining small at its core, multiple
document editing through the use of a 'tabbed' notebook and
many more functions.

%package devel
Group: Development/C
Summary: Headers for writing gEdit plugins

%description devel
gEdit is a small but powerful text editor designed expressly
for GNOME.

It includes such features as split-screen mode, a plugin
API, which allows gEdit to be extended to support many
features while remaining small at its core, multiple
document editing through the use of a 'tabbed' notebook and
many more functions.

Install this if you want to build plugins that use gEdit's API.

%prep
%setup -q
%patch -p1
%patch1 -p1 -b .encoding
%patch4 -p1 -b .filesel

%build
%configure2_5x --enable-gtk-doc \
%if %{build_with_python}
--enable-python
%else
--disable-python
%endif

make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
rm -rf %buildroot/var
%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name-2.0.lang
done

# menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):\
	needs="X11" \
	section="More Applications/Editors" \
	title="GEdit" \
	longtitle="GEdit is a small but powerful text editor" \
	command="%{_bindir}/gedit" \
	icon="text-editor" \
	startup_notify="true" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-MoreApplications-Editors" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la \
 $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper
%post_install_gconf_schemas gedit
%update_desktop_database
%{update_menus}

%preun
%preun_uninstall_gconf_schemas gedit

%postun 
%{clean_menus}
%clean_scrollkeeper
%clean_desktop_database

%files -f %{name}-2.0.lang
%defattr(-, root, root)
%doc README AUTHORS NEWS MAINTAINERS
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%dir %{_libdir}/gedit-2
%dir %{_libdir}/gedit-2/plugins
%{_libdir}/gedit-2/gedit-bugreport.sh
%{_libdir}/gedit-2/plugins/*.so
%{_libdir}/gedit-2/plugins/*.gedit-plugin
%{_libdir}/gedit-2/plugins/externaltools/
%{_libdir}/gedit-2/plugins/snippets/
%{_libdir}/gedit-2/plugins/pythonconsole/
%{_datadir}/gedit-2
%{_datadir}/applications/*
%dir %{_datadir}/omf/gedit
%{_datadir}/omf/gedit/*-C.omf
%{_menudir}/*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%_datadir/gtk-doc/html/*
