# **********************************************************************
#
# Copyright (c) 2003-2009 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

%if "%{dist}" == ".rhel4" || "%{dist}" == ".rhel5"
  %define ruby 1
  %define mono 0
%else
  %if "%{dist}" == ".sles10"
    %define ruby 0
    %define mono 1
  %else
    %define ruby 0
    %define mono 0
  %endif
%endif

%define buildall 1
%define makeopts -j2

%define core_arches %{ix86} x86_64

#
# See http://fedoraproject.org/wiki/Packaging/Python
#
# We put everything in sitearch because we're building a single
# ice-python arch-specific package.
#
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if %{ruby}
#
# See http://fedoraproject.org/wiki/Packaging/Ruby
#
# We put everything in sitearch because we're building a single
# ice-ruby arch-specific package.
#
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}
%endif

Name: ice
Version: 3.3.1
Summary: Files common to all Ice packages 
Release: 1%{?dist}
License: GPL with exceptions
Group: System Environment/Libraries
Vendor: ZeroC, Inc.
URL: http://www.zeroc.com/
Source0: Ice-%{version}.tar.gz
Source1: Ice-rpmbuild-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define soversion 33
%define dotnetversion 3.3.1
%define dotnetpolicyversion 3.3

%define formsversion 1.2.0
%define looksversion 2.1.4
%define dbversion 4.6.21

BuildRequires: openssl-devel >= 0.9.7a
BuildRequires: db46-devel >= 4.6.21, db46-java >= 4.6.21
BuildRequires: jpackage-utils
BuildRequires: mcpp-devel >= 2.7.2

#
# Prerequisites for building Ice for Java:
#
# - a recent version of ant
# - %{_javadir}/jgoodies-forms-%{formsversion}.jar
# - %{_javadir}/jgoodies-forms-%{looksversion}.jar
# - %{_javadir}/proguard.jar
#
# Use find-jar to verify that the JAR files are present:
#
# $ find-jar proguard.jar
#

%if %{ruby}
BuildRequires: ruby-devel
%endif

%if %{mono}
BuildRequires: mono-core >= 1.2.6, mono-devel >= 1.2.6
%endif

%if "%{dist}" == ".rhel4"
BuildRequires: nptl-devel
BuildRequires: bzip2-devel >= 1.0.2
BuildRequires: expat-devel >= 1.95.7
BuildRequires: php-devel >= 5.1.4
BuildRequires: python-devel >= 2.3.4
%endif
%if "%{dist}" == ".rhel5"
BuildRequires: bzip2-devel >= 1.0.3
BuildRequires: expat-devel >= 1.95.8
BuildRequires: php-devel >= 5.1.6
BuildRequires: python-devel >= 2.4.3
%endif
%if "%{dist}" == ".sles10"
BuildRequires: php5-devel >= 5.1.2
BuildRequires: python-devel >= 2.4.2
%endif

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+.  It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, .NET, Java,
Python, Ruby, and PHP mappings, a highly efficient protocol, 
asynchronous method invocation and dispatch, dynamic transport 
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.

#
# We create both noarch and arch-specific packages for these GAC files.
# Please delete the arch-specific packages after the build: we create
# them only to keep rpmbuild happy (it does not want to create dangling
# symbolic links (the GAC symlinks used for development)).
#
%if %{mono}
%package mono
Summary: The Ice runtime for .NET (mono)
Group: System Environment/Libraries
Requires: ice = %{version}-%{release}, mono-core >= 1.2.2
Obsoletes: ice-dotnet < %{version}-%{release}
%description mono
The Ice runtime for .NET (mono).
%endif

#
# Arch-independent packages
#
%ifarch noarch
%package java
Summary: The Ice runtime for Java
Group: System Environment/Libraries
Requires: ice = %{version}-%{release}, db46-java,
%description java
The Ice runtime for Java.
%endif

#
# Arch-dependent packages
#
%ifarch %{core_arches}
%package libs
Summary: The Ice runtime for C++
Group: System Environment/Libraries
Requires: ice = %{version}-%{release}, db46
%description libs
The Ice runtime for C++

%package utils
Summary: Ice utilities and admin tools.
Group: Applications/System
Requires: ice-libs = %{version}-%{release}
%description utils
Admin tools to manage Ice servers (IceGrid, IceStorm, IceBox etc.),
plus various Ice-related utilities.

%package servers
Summary: Ice servers and related files.
Group: System Environment/Daemons
Requires: ice-utils = %{version}-%{release}
%if %{mono}
Requires: ice-mono = %{version}-%{release}
%endif
# Requirements for the users
%if "%{dist}" == ".sles10"
Requires(pre): pwdutils
%endif
%if "%{dist}" == ".rhel4" || "%{dist}" == ".rhel5"
Requires(pre): shadow-utils
%endif
# Requirements for the init.d services
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%description servers
Ice servers: glacier2router, icebox, icegridnode, icegridregistry, 
icebox, iceboxnet, icepatch2server and related files.

%package c++-devel
Summary: Tools, libraries and headers for developing Ice applications in C++
Group: Development/Tools
Requires: ice-libs = %{version}-%{release}
%if "%{dist}" == ".rhel4"
Requires: nptl-devel
%endif
%description c++-devel
Tools, libraries and headers for developing Ice applications in C++.

%package java-devel
Summary: Tools for developing Ice applications in Java
Group: Development/Tools
Requires: ice-java = %{version}-%{release}, ice-libs = %{version}-%{release}
%description java-devel
Tools for developing Ice applications in Java.

%if %{mono}
%package mono-devel
Summary: Tools for developing Ice applications in C#
Group: Development/Tools
Requires: ice-mono = %{version}-%{release}, ice-libs = %{version}-%{release}, pkgconfig
Obsoletes: ice-csharp-devel < %{version}-%{release}
%description mono-devel
Tools for developing Ice applications in C#.
%endif

%if %{ruby}
%package ruby
Summary: The Ice runtime for Ruby
Group: System Environment/Libraries
Requires: ice-libs = %{version}-%{release}, ruby
%description ruby
The Ice runtime for Ruby.

%package ruby-devel
Summary: Tools for developing Ice applications in Ruby
Group: Development/Tools
Requires: ice-ruby = %{version}-%{release}
%description ruby-devel
Tools for developing Ice applications in Ruby.
%endif

%package python
Summary: The Ice runtime for Python
Group: System Environment/Libraries
Requires: ice-libs = %{version}-%{release}
%description python
The Ice runtime for Python.

%package python-devel
Summary: Tools for developing Ice applications in Python
Group: Development/Tools
Requires: ice-python = %{version}-%{release}
%description python-devel
Tools for developing Ice applications in Python.

%package php
Summary: The Ice runtime for PHP
Group: System Environment/Libraries
Requires: ice = %{version}-%{release}
%description php
The Ice runtime for PHP.
%endif


%prep

%if %{buildall}
%setup -n Ice-%{version} -q
%setup -q -n Ice-rpmbuild-%{version} -T -b 1
%endif

%build

#
# We build C++ all the time since we need slice2xxx
#
cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src
make %{makeopts} OPTIMIZE=yes embedded_runpath_prefix=""

%ifarch %{core_arches}
cd $RPM_BUILD_DIR/Ice-%{version}/py
make %{makeopts} OPTIMIZE=yes embedded_runpath_prefix=""

cd $RPM_BUILD_DIR/Ice-%{version}/php
make %{makeopts} OPTIMIZE=yes embedded_runpath_prefix=""

%if %{ruby}
cd $RPM_BUILD_DIR/Ice-%{version}/rb
make %{makeopts} OPTIMIZE=yes embedded_runpath_prefix=""
%endif

%endif

#
# We build java5 all the time, since we include the GUI and
# ant-ice.jar in a non-noarch package.
#
cd $RPM_BUILD_DIR/Ice-%{version}/java
export CLASSPATH=`build-classpath db-%{dbversion} jgoodies-forms-%{formsversion} jgoodies-looks-%{looksversion} proguard`
JGOODIES_FORMS=`find-jar jgoodies-forms-%{formsversion}`
JGOODIES_LOOKS=`find-jar jgoodies-looks-%{looksversion}`

ant -Dice.mapping=java5 -Dbuild.suffix=java5 -Djgoodies.forms=$JGOODIES_FORMS -Djgoodies.looks=$JGOODIES_LOOKS jar

%ifarch noarch
ant -Dice.mapping=java2 -Dbuild.suffix=java2 jar
%endif

# 
# We build mono all the time because we include iceboxnet.exe in an
# arch-specific package; we also include GAC symlinks in another
# arch-specific package.
#
# Define the environment variable KEYFILE to strong-name sign the
# assemblies your own key file.
#

%if %{mono}
cd $RPM_BUILD_DIR/Ice-%{version}/cs/src
make %{makeopts} OPTIMIZE=yes
%endif


%install

rm -rf $RPM_BUILD_ROOT

#
# Arch-specific packages
#
%ifarch %{core_arches}

#
# C++
#
mkdir -p $RPM_BUILD_ROOT/lib

cd $RPM_BUILD_DIR/Ice-%{version}/cpp
make prefix=$RPM_BUILD_ROOT embedded_runpath_prefix="" install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
mv $RPM_BUILD_ROOT/lib/ImportKey.class $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%_lib/* $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/include/* $RPM_BUILD_ROOT%{_includedir}

#
# Python
#
cd $RPM_BUILD_DIR/Ice-%{version}/py
make prefix=$RPM_BUILD_ROOT embedded_runpath_prefix="" install

mkdir -p $RPM_BUILD_ROOT%{python_sitearch}/Ice
mv $RPM_BUILD_ROOT/python/* $RPM_BUILD_ROOT%{python_sitearch}/Ice
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.pth $RPM_BUILD_ROOT%{python_sitearch}

#
# PHP
#
cd $RPM_BUILD_DIR/Ice-%{version}/php
make prefix=$RPM_BUILD_ROOT install

%if "%{dist}" == ".rhel4" || "%{dist}" == ".rhel5"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php/modules
mv $RPM_BUILD_ROOT/%_lib/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php/modules
%endif

%if "%{dist}" == ".sles10"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php5/extensions
mv $RPM_BUILD_ROOT/%_lib/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php5/extensions
%endif

#
# Ruby
# 
%if %{ruby}
cd $RPM_BUILD_DIR/Ice-%{version}/rb
make prefix=$RPM_BUILD_ROOT embedded_runpath_prefix="" install
mkdir -p $RPM_BUILD_ROOT%{ruby_sitearch}
mv $RPM_BUILD_ROOT/ruby/* $RPM_BUILD_ROOT%{ruby_sitearch}
%else
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2rb
%endif

#
# IceGridGUI
#
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/libjava5/IceGridGUI.jar $RPM_BUILD_ROOT%{_javadir}/IceGridGUI-%{version}.jar
ln -s IceGridGUI-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/IceGridGUI.jar 
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/bin/icegridgui.rpm $RPM_BUILD_ROOT%{_bindir}/icegridgui
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/help
cp -Rp $RPM_BUILD_DIR/Ice-%{version}/java/resources/IceGridAdmin $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/help

#
# ant-ice.jar
#
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/libjava5/ant-ice.jar $RPM_BUILD_ROOT%{_javadir}/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/ant-ice.jar 


%if %{mono}

#
# Mono: for iceboxnet.exe and GAC symlinks
#
cd $RPM_BUILD_DIR/Ice-%{version}/cs
make prefix=$RPM_BUILD_ROOT GACINSTALL=yes GAC_ROOT=$RPM_BUILD_ROOT%{_prefix}/lib install
mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}

#
# .NET spec files (for mono-devel)
#
if test ! -d $RPM_BUILD_ROOT%{_libdir}/pkgconfig
then
    mv $RPM_BUILD_ROOT/lib/pkgconfig $RPM_BUILD_ROOT%{_libdir}
fi
%endif

#
# initrd files (for servers)
#
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
for i in icegridregistry icegridnode glacier2router
do
    cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/$i.%{_vendor} $RPM_BUILD_ROOT%{_initrddir}/$i
done

#
# Some python scripts and related files
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
mv $RPM_BUILD_ROOT/config/* $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}

#
# Cleanup extra files
#
rm -f $RPM_BUILD_ROOT/ICE_LICENSE
rm -f $RPM_BUILD_ROOT/LICENSE
rm -fr $RPM_BUILD_ROOT/doc/reference
rm -fr $RPM_BUILD_ROOT/slice
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceStormService.so

%if !%{mono}
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2cs
%endif

%endif

#
# Arch-independent packages
#
%ifarch noarch

#
# Doc
#
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp -p $RPM_BUILD_DIR/Ice-%{version}/RELEASE_NOTES $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/RELEASE_NOTES
cp -p $RPM_BUILD_DIR/Ice-%{version}/CHANGES $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/CHANGES
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/README.Linux-RPM $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/README
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/THIRD_PARTY_LICENSE.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/THIRD_PARTY_LICENSE
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/SOURCES.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/SOURCES

#
# Java install (using jpackage conventions)
# 
cd $RPM_BUILD_DIR/Ice-%{version}/java
ant -Dice.mapping=java5 -Dbuild.suffix=java5 -Dprefix=$RPM_BUILD_ROOT install
ant -Dice.mapping=java2 -Dbuild.suffix=java2 -Dprefix=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
mv $RPM_BUILD_ROOT/lib/Ice.jar $RPM_BUILD_ROOT%{_javadir}/Ice-%{version}.jar
ln -s  Ice-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Ice.jar 
mv $RPM_BUILD_ROOT/lib/java2/Ice.jar $RPM_BUILD_ROOT%{_javadir}/Ice-java2-%{version}.jar
ln -s Ice-java2-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/Ice-java2.jar


%if %{mono}
#
# Mono
#
cd $RPM_BUILD_DIR/Ice-%{version}/cs
make prefix=$RPM_BUILD_ROOT GACINSTALL=yes GAC_ROOT=$RPM_BUILD_ROOT%{_prefix}/lib install
%endif

#
# License files
#
mv $RPM_BUILD_ROOT/ICE_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT/LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

#
# Slice  files
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
mv $RPM_BUILD_ROOT/slice $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}

#
# Cleanup extra files
#
rm -fr $RPM_BUILD_ROOT/help
rm -f $RPM_BUILD_ROOT/lib/IceGridGUI.jar $RPM_BUILD_ROOT/lib/ant-ice.jar
%if %{mono}
rm -f $RPM_BUILD_ROOT/bin/iceboxnet.exe

for f in Ice Glacier2 IceBox IceGrid IcePatch2 IceStorm
do 
     rm -r $RPM_BUILD_ROOT%{_prefix}/lib/mono/$f
done

rm -r $RPM_BUILD_ROOT/lib/pkgconfig

%endif

%endif


%clean
rm -rf $RPM_BUILD_ROOT

#
# mono package; see comment above about why we create
# "useless" arch-specific packages
#
%if %{mono}
%files mono
%defattr(-, root, root, -)
%dir %{_prefix}/lib/mono/gac/Glacier2
%{_prefix}/lib/mono/gac/Glacier2/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/Ice
%{_prefix}/lib/mono/gac/Ice/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/IceBox
%{_prefix}/lib/mono/gac/IceBox/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/IceGrid
%{_prefix}/lib/mono/gac/IceGrid/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/IcePatch2
%{_prefix}/lib/mono/gac/IcePatch2/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/IceStorm
%{_prefix}/lib/mono/gac/IceStorm/%{dotnetversion}.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.Glacier2
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.Glacier2/0.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.Ice
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.Ice/0.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceBox
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceBox/0.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceGrid
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceGrid/0.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IcePatch2
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IcePatch2/0.*/
%dir %{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceStorm
%{_prefix}/lib/mono/gac/policy.%{dotnetpolicyversion}.IceStorm/0.*/
%endif

#
# noarch file packages
# 
%ifarch noarch
%files
%defattr(-, root, root, -)
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/slice
%{_defaultdocdir}/%{name}-%{version}

%files java
%defattr(-, root, root, -)
%{_javadir}/Ice-%{version}.jar
%{_javadir}/Ice.jar
%{_javadir}/Ice-java2-%{version}.jar
%{_javadir}/Ice-java2.jar
%endif

#
# arch-specific packages
#
%ifarch %{core_arches}
%files libs
%defattr(-, root, root, -)
%{_libdir}/libFreeze.so.%{version}
%{_libdir}/libFreeze.so.%{soversion}
%{_libdir}/libGlacier2.so.%{version}
%{_libdir}/libGlacier2.so.%{soversion}
%{_libdir}/libIceBox.so.%{version}
%{_libdir}/libIceBox.so.%{soversion}
%{_libdir}/libIcePatch2.so.%{version}
%{_libdir}/libIcePatch2.so.%{soversion}
%{_libdir}/libIce.so.%{version}
%{_libdir}/libIce.so.%{soversion}
%{_libdir}/libIceSSL.so.%{version}
%{_libdir}/libIceSSL.so.%{soversion}
%{_libdir}/libIceStorm.so.%{version}
%{_libdir}/libIceStorm.so.%{soversion}
%{_libdir}/libIceUtil.so.%{version}
%{_libdir}/libIceUtil.so.%{soversion}
%{_libdir}/libSlice.so.%{version}
%{_libdir}/libSlice.so.%{soversion}
%{_libdir}/libIceGrid.so.%{version}
%{_libdir}/libIceGrid.so.%{soversion}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files utils
%defattr(-, root, root, -)
%{_libdir}/libIceXML.so.%{version}
%{_libdir}/libIceXML.so.%{soversion}
%{_bindir}/dumpdb
%{_bindir}/transformdb
%{_bindir}/iceboxadmin
%{_bindir}/icepatch2calc
%{_bindir}/icepatch2client
%{_bindir}/icestormadmin
%{_bindir}/slice2docbook
%{_bindir}/slice2html
%{_bindir}/icegridadmin
%{_bindir}/icegridgui
%{_bindir}/iceca
%{_javadir}/IceGridGUI-%{version}.jar
%{_javadir}/IceGridGUI.jar
%dir %{_defaultdocdir}/%{name}-%{version}
%{_defaultdocdir}/%{name}-%{version}/help
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/ImportKey.class
%attr(755,root,root) %{_datadir}/Ice-%{version}/convertssl.py*

%post utils -p /sbin/ldconfig
%postun utils -p /sbin/ldconfig

%files servers
%defattr(-, root, root, -)
%{_bindir}/glacier2router
%{_bindir}/icebox
%if %{mono}
%{_bindir}/iceboxnet.exe
%endif
%{_bindir}/icegridnode
%{_bindir}/icegridregistry
%{_bindir}/icepatch2server
%{_bindir}/icestormmigrate
%{_libdir}/libIceStormService.so.%{version}
%{_libdir}/libIceStormService.so.%{soversion}
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/templates.xml
%attr(755,root,root) %{_datadir}/Ice-%{version}/upgradeicegrid.py*
%{_datadir}/Ice-%{version}/icegrid-slice.3.1.ice.gz
%{_datadir}/Ice-%{version}/icegrid-slice.3.2.ice.gz
%{_datadir}/Ice-%{version}/icegrid-slice.3.3.ice.gz
%attr(755,root,root) %{_initrddir}/icegridregistry
%attr(755,root,root) %{_initrddir}/icegridnode
%attr(755,root,root) %{_initrddir}/glacier2router
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %{_sysconfdir}/glacier2router.conf

%pre servers
getent group ice > /dev/null || groupadd -r ice
getent passwd ice > /dev/null || \
       useradd -r -g ice -d %{_localstatedir}/lib/ice \
       -s /sbin/nologin -c "Ice Service account" ice
test -d %{_localstatedir}/lib/ice/icegrid/registry || \
       mkdir -p %{_localstatedir}/lib/ice/icegrid/registry; chown -R ice.ice %{_localstatedir}/lib/ice
test -d %{_localstatedir}/lib/ice/icegrid/node1 || \
       mkdir -p %{_localstatedir}/lib/ice/icegrid/node1; chown -R ice.ice %{_localstatedir}/lib/ice
exit 0

%post servers
/sbin/ldconfig
%if "%{dist}" != ".sles10"
/sbin/chkconfig --add icegridregistry
/sbin/chkconfig --add icegridnode
/sbin/chkconfig --add glacier2router
%endif

%preun servers
if [ $1 = 0 ]; then
%if "%{dist}" == ".sles10"
        /sbin/service icegridnode stop >/dev/null 2>&1 || :
        /sbin/insserv -r icegridnode
	/sbin/service icegridregistry stop >/dev/null 2>&1 || :
        /sbin/insserv -r icegridregistry
        /sbin/service glacier2router stop >/dev/null 2>&1 || :
        /sbin/insserv -r glacier2router
%else
        /sbin/service icegridnode stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del icegridnode
	/sbin/service icegridregistry stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del icegridregistry
        /sbin/service glacier2router stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del glacier2router
%endif
fi

%postun servers
if [ "$1" -ge "1" ]; then
        /sbin/service icegridnode condrestart >/dev/null 2>&1 || :
	/sbin/service icegridregistry condrestart >/dev/null 2>&1 || :
        /sbin/service glacier2router condrestart >/dev/null 2>&1 || :
fi
/sbin/ldconfig

%files c++-devel
%defattr(-, root, root, -)

%{_bindir}/slice2cpp
%{_bindir}/slice2freeze
%{_includedir}/Freeze
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_includedir}/IceXML
%{_includedir}/Slice
%{_libdir}/libFreeze.so
%{_libdir}/libGlacier2.so
%{_libdir}/libIceBox.so
%{_libdir}/libIceGrid.so
%{_libdir}/libIcePatch2.so
%{_libdir}/libIce.so
%{_libdir}/libIceSSL.so
%{_libdir}/libIceStorm.so
%{_libdir}/libIceUtil.so
%{_libdir}/libIceXML.so
%{_libdir}/libSlice.so


%if %{mono}
%files mono-devel
%defattr(-, root, root, -)
%{_bindir}/slice2cs
%{_libdir}/pkgconfig/Ice.pc
%{_libdir}/pkgconfig/Glacier2.pc
%{_libdir}/pkgconfig/IceBox.pc
%{_libdir}/pkgconfig/IceGrid.pc
%{_libdir}/pkgconfig/IcePatch2.pc
%{_libdir}/pkgconfig/IceStorm.pc
%{_prefix}/lib/mono/Glacier2/
%{_prefix}/lib/mono/Ice/
%{_prefix}/lib/mono/IceBox/
%{_prefix}/lib/mono/IceGrid/
%{_prefix}/lib/mono/IcePatch2/
%{_prefix}/lib/mono/IceStorm/
%endif

%files java-devel
%defattr(-, root, root, -)
%{_bindir}/slice2java
%{_bindir}/slice2freezej
%{_javadir}/ant-ice-%{version}.jar
%{_javadir}/ant-ice.jar

%files python
%defattr(-, root, root, -)
%{python_sitearch}/Ice
%{python_sitearch}/ice.pth

%files python-devel
%defattr(-, root, root, -)
%{_bindir}/slice2py

%if %{ruby}
%files ruby
%defattr(-, root, root, -)
%{ruby_sitearch}/*

%files ruby-devel
%defattr(-, root, root, -)
%{_bindir}/slice2rb
%endif

%files php
%defattr(-, root, root, -)

%if "%{dist}" == ".rhel4" || "%{dist}" == ".rhel5"
%{_libdir}/php/modules/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif

%if "%{dist}" == ".sles10"
%{_libdir}/php5/extensions
%config(noreplace) %{_sysconfdir}/php5/conf.d/ice.ini
%endif
%endif


%changelog

* Wed Mar 4 2009 Bernard Normier <bernard@zeroc.com> 3.3.1
- Minor updates for the Ice 3.3.1 release.

* Wed Feb 27 2008 Bernard Normier <bernard@zeroc.com> 3.3b-1
- Updates for Ice 3.3b release:
 - Split main ice rpm into ice noarch (license and Slice files), ice-libs 
   (C++ runtime libraries), ice-utils (admin tools & utilities), ice-servers
   (icegridregistry, icebox etc.). This way, ice-libs 3.3.0 can coexist with
    ice-libs 3.4.0. The same is true for ice-mono, and to a lesser extent 
    other ice runtime packages
- Many updates derived from Mary Ellen Foster (<mefoster at gmail.com>)'s 
  Fedora RPM spec for Ice.
 - The Ice jar files are now installed in %{_javalibdir}, with 
   jpackage-compliant names
 - New icegridgui shell script to launch the IceGrid GUI
 - The .NET files are now packaged using gacutil with the -root option.
 - ice-servers creates a new user (ice) and installs three init.d services:
   icegridregistry, icegridnode and glacier2router.
 - Python, Ruby and PHP files are now installed in the correct directories.

* Fri Jul 27 2007 Bernard Normier <bernard@zeroc.com> 3.2.1-1
- Updated for Ice 3.2.1 release

* Wed Jun 13 2007 Bernard Normier <bernard@zeroc.com>
- Added patch with new IceGrid.Node.AllowRunningServersAsRoot property.

* Fri Dec 6 2006 ZeroC Staff <support@zeroc.com>
- See source distributions or the ZeroC website for more information
  about the changes in this release
