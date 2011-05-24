#Module-Specific definitions
%define mod_name mod_umask
%define mod_conf A81_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_umask sets the Unix umask of the Apache HTTPd process after it has started
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	%mkrel 10
Group:		System/Servers
License:	GPL
URL:		http://www.outoforder.cc/projects/apache/mod_umask/
Source0:	http://www.outoforder.cc/downloads/mod_umask/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_umask-0.1.0-module.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_umask sets the Unix umask of the Apache HTTPd process after it has started.
This is useful when accessing Subversion from both mod_dav_svn and via a local
client with a // url. Without setting a proper umask the file permissions can
create a repository that is not easily accessable from both. 

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p1

# stupid libtool...
perl -pi -e "s|libmod_umask|mod_umask|g" src/Makefile*

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" *

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure2_5x --localstatedir=/var/lib

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


