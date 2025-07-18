%define url_ver %(echo %{version}|cut -d. -f1,2)

%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define build_python 1

Summary:	Small but powerful text editor for GNOME
Name:		gedit
Version:	48.2
Release:	1
License:	GPLv2+
Group:		Editors
Url:		https://gedit-technology.github.io/apps/gedit/
#Source0:	https://ftp.gnome.org/pub/GNOME/sources/gedit/%{url_ver}/%{name}-%{version}.tar.xz
Source0:  https://gitlab.gnome.org/World/gedit/gedit/-/archive/%{version}/gedit-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	meson
BuildRequires:	python-gi
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(enchant)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.25.5
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(libgedit-gtksourceview-300)
BuildRequires:	pkgconfig(gspell-1)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libpeas-gtk-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  pkgconfig(libgedit-tepl-6)
BuildRequires:  yelp-tools
BuildRequires:  gtk-doc
BuildRequires:  gettext-devel
%if %{build_python}
BuildRequires:	python3-devel
BuildRequires:	python-gi
BuildRequires:	pkgconfig(pygobject-3.0)
%endif

Requires:  %{_lib}tepl

Obsoletes:	%{_lib}gedit-private0 < 3.4.2
Obsoletes:	%{name} < %{EVRD}

%description
gEdit is a small but powerful text editor designed expressly
for GNOME.

It includes such features as split-screen mode, a plugin
API, which allows gEdit to be extended to support many
features while remaining small at its core, multiple
document editing through the use of a 'tabbed' notebook and
many more functions.

%package devel
Group:		Development/C
Summary:	Headers for writing gEdit plugins
Requires:       %{name} = %{version}-%{release}
Obsoletes:	%{_lib}gedit-private-devel < 3.4.2

%description devel
Install this if you want to build plugins that use gEdit's API.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson -Duser_documentation=true
%meson_build

%install
%meson_install

rm -Rf %{buildroot}%{py3_platsitedir}/gi/overrides/__pycache__

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc README.md NEWS
%{_bindir}/*
%{_datadir}/applications/org.gnome.gedit.desktop
%{_datadir}/metainfo/org.gnome.gedit.metainfo.xml
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/gedit
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.spell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
#{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
#{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_mandir}/man1/gedit.1*
%{_datadir}/icons/*/*/*/*

#{_libexecdir}/gedit/gedit-bugreport.sh
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%{_libdir}/gedit/libgedit*.so
%{_libdir}/gedit/plugins/libtextsize.so
%{_libdir}/gedit/plugins/libquickhighlight.so
%{_libdir}/gedit/plugins/quickhighlight.plugin

%{_libdir}/gedit/plugins/libdocinfo.so
%{_libdir}/gedit/plugins/docinfo.plugin

%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/libfilebrowser.so

%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/libmodelines.so

%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/libsort.so

%{_libdir}/gedit/plugins/time.plugin
%{_libdir}/gedit/plugins/libtime.so

%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/libspell.so

%if %{build_python}
%{python_sitelib}/gi/overrides/Gedit.py
%{python_sitelib}/gi/overrides/__pycache__/Gedit.cpython-*.pyc

#{_libdir}/gedit/plugins/pythonconsole/*
#{_libdir}/gedit/plugins/pythonconsole.plugin

%{_libdir}/gedit/plugins/textsize.plugin
#{_libdir}/gedit/plugins/textsize/__init__.py
#{_libdir}/gedit/plugins/textsize/signals.py
#{_libdir}/gedit/plugins/textsize/viewactivatable.py
%endif

%files devel
%doc %{_datadir}/gtk-doc/html/gedit/
%{_includedir}/*
%{_libdir}/pkgconfig/*
#{_datadir}/vala/vapi/gedit.deps
#{_datadir}/vala/vapi/gedit.vapi

#exclude /usr/lib*/debug/usr/lib*/gedit/plugins/libquickhighlight.so-%{version}.*.debug
