%define url_ver %(echo %{version}|cut -d. -f1,2)

%define _disable_ld_no_undefined 1
%define build_python 1

Summary:	Small but powerful text editor for GNOME
Name:		gedit
Version:	3.8.3
Release:	4
License:	GPLv2+
Group:		Editors 
Url:		http://www.gnome.org/projects/gedit/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gedit/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	python-gi
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(enchant)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libpeas-gtk-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zeitgeist-2.0)
%if %{build_python}
BuildRequires:	python3-devel
BuildRequires:	python3-gi
BuildRequires:	pkgconfig(pygobject-3.0)
%endif

Obsoletes:	%{_lib}gedit-private0 < 3.4.2

%description
gEdit is a small but powerful text editor designed expressly
for GNOME.

It includes such features as split-screen mode, a plugin
API, which allows gEdit to be extended to support many
features while remaining small at its core, multiple
document editing through the use of a 'tabbed' notebook and
many more functions.

%package zeitgeist
Summary:	Zeitgeist plugin for gedit
Group:		Editors
Requires:	%{name} = %{version}-%{release}

%description zeitgeist
This packages brings the Zeitgeist dataprovider - a plugin that logs
access and leave event for documents used with gedit.

%package devel
Group:		Development/C
Summary:	Headers for writing gEdit plugins
Obsoletes:	%{_lib}gedit-private-devel < 3.4.2

%description devel
Install this if you want to build plugins that use gEdit's API.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--enable-gtk-doc \
%if %{build_python}
	--enable-python \
%else
	--disable-python \
%endif
	--enable-introspection \
	--disable-updater \
	--enable-gvfs-metadata

%make LIBS='-lm'

%install
%makeinstall_std

sed -i 's,Keywords.*,&;,g' %{buildroot}%{_datadir}/applications/gedit.desktop

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc README AUTHORS NEWS MAINTAINERS
%{_bindir}/*
%{_datadir}/applications/gedit.desktop
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/GConf/gsettings/gedit.*
%{_datadir}/gedit

%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_mandir}/man1/gedit.1*

%{_libdir}/gedit/gedit-bugreport.sh
%{_libdir}/gedit/girepository-1.0/Gedit-3.0.typelib
%{_libdir}/gedit/libgedit-private.so

%{_libdir}/gedit/plugins/changecase.plugin
%{_libdir}/gedit/plugins/libchangecase.so

%{_libdir}/gedit/plugins/libdocinfo.so
%{_libdir}/gedit/plugins/docinfo.plugin

%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/libfilebrowser.so

%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/libmodelines.so

%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/libsort.so

%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/libspell.so

%{_libdir}/gedit/plugins/time.plugin
%{_libdir}/gedit/plugins/libtime.so

%if %{build_python}
%{python3_sitearch}/gi/overrides/Gedit.*
%{_libdir}/gedit/plugins/externaltools/*
%{_libdir}/gedit/plugins/externaltools.plugin

%{_libdir}/gedit/plugins/pythonconsole/*
%{_libdir}/gedit/plugins/pythonconsole.plugin

%{_libdir}/gedit/plugins/quickopen/*
%{_libdir}/gedit/plugins/quickopen.plugin

%{_libdir}/gedit/plugins/snippets/*
%{_libdir}/gedit/plugins/snippets.plugin
%endif

%files zeitgeist
%{_libdir}/gedit/plugins/zeitgeist.plugin
%{_libdir}/gedit/plugins/libzeitgeistplugin.so

%files devel
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/pkgconfig/*

