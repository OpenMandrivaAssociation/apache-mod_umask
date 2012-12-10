#Module-Specific definitions
%define mod_name mod_umask
%define mod_conf A81_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_umask sets the Unix umask of the Apache HTTPd process after it has started
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	10
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

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-10mdv2011.0
+ Revision: 678430
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2011.0
+ Revision: 588076
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2010.1
+ Revision: 516201
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2010.0
+ Revision: 406664
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2009.0
+ Revision: 235115
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2009.0
+ Revision: 215657
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2008.1
+ Revision: 181937
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2008.0
+ Revision: 82688
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2007.1
+ Revision: 140766
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2007.0
+ Revision: 79531
- Import apache-mod_umask

* Wed Aug 02 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2007.0
- initial Mandriva package

