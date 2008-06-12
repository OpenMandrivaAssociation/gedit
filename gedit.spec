%define build_with_python 1
Summary:		Small but powerful text editor for GNOME
Name:			gedit
Version: 2.22.3
Release: %mkrel 1
License:		GPL
Group:			Editors 
Source0:		ftp://ftp.gnome.org/pub/GNOME/sources/gedit/%{name}-%{version}.tar.bz2
# (fc) use current locale when creating new file (Mdk bug 6887), detect if content is current locale or UTF-8 on file load (Mdv bug #20277) (Antoine Pitrou)
Patch0:			gedit-2.19.92-localencoding.patch
URL:			http://www.gnome.org/projects/gedit/
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	gtksourceview-devel >= 2.2.0
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
BuildRequires: python-gtksourceview-devel >= 2.2.0
BuildRequires: libglade2.0-devel
BuildRequires: librsvg
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
%patch0 -p1 -b .localencoding

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

mkdir -p %buildroot%{_miconsdir} %buildroot%{_liconsdir} %buildroot%{_iconsdir} 

cp %{_datadir}/icons/gnome/16x16/apps/accessories-text-editor.png %buildroot%{_miconsdir}/accessories-text-editor.png
rsvg -w 32 -h 32 %{_datadir}/icons/gnome/scalable/apps/accessories-text-editor.svn %buildroot%{_iconsdir}/accessories-text-editor.png
rsvg -w 48 -h 48 %{_datadir}/icons/gnome/scalable/apps/accessories-text-editor.svn %buildroot%{_liconsdir}/accessories-text-editor.png

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la \
 $RPM_BUILD_ROOT%{_libdir}/bonobo/*.la $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_scrollkeeper
%post_install_gconf_schemas gedit
%update_desktop_database
%{update_menus}
%endif

%preun
%preun_uninstall_gconf_schemas gedit

%if %mdkversion < 200900
%postun 
%{clean_menus}
%clean_scrollkeeper
%clean_desktop_database
%endif

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
%{_mandir}/man1/*
%{_liconsdir}/*.png
%{_iconsdir}/*.png
%{_miconsdir}/*.png

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%_datadir/gtk-doc/html/*
