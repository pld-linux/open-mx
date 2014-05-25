# TODO: finish PLDizing kernel module package
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# kernel module
%bcond_without	userspace	# userspace programs

%if %{without kernel}
%undefine	with_dist_kernel
%endif
Summary:	OpenMX - Myrinet Express over generic Ethernet hardware
Summary(pl.UTF-8):	OpenMX - Myrinet Express po zwykłym sprzęcie ethernetowym
Name:		open-mx
Version:	1.5.3
Release:	0.1
License:	GPL v2 (tools), LGPL v2.1 (libraries)
Group:		Applications
Source0:	http://gforge.inria.fr/frs/download.php/32114/%{name}-%{version}.tar.gz
# Source0-md5:	b0eb065f7df5aa888fd4d15846b7b023
URL:		http://open-mx.org/
BuildRequires:	hwloc-devel >= 1.0
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open-MX is a high-performance implementation of the Myrinet Express
message-passing stack over generic Ethernet networks. It provides
application-level and wire-protocol compatibility with the native MXoE
(Myrinet Express over Ethernet) stack.

%description -l pl.UTF-8
Open-MX to wysoko wydajna implementacja stosu przekazywania
komunikatów Myrinet Express po zwykłych sieciach Ethernet. Zapewnia
zgodność na poziomie aplikacji oraz protokołu sieciowego z natywnym
stosem MXoE (Myrinet Express over Ethernet).

%package libs
Summary:	Open-MX library
Summary(pl.UTF-8):	Biblioteka Open-MX
Group:		Libraries

%description libs
Open-MX library.

%description libs -l pl.UTF-8
Biblioteka Open-MX.

%package devel
Summary:	Header files for Open-MX library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Open-MX
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Open-MX library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Open-MX.

%package static
Summary:	Static Open-MX library
Summary(pl.UTF-8):	Statyczna biblioteka Open-MX
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Open-MX library.

%description static -l pl.UTF-8
Statyczna biblioteka Open-MX.

%package -n kernel%{_alt_kernel}-misc-open-mx
Summary:	Linux driver for Open-MX
Summary(pl.UTF-8):	Sterownik Open-MX dla Linuksa
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-open-mx
Linux driver for Open-MX.

%description -n kernel%{_alt_kernel}-misc-open-mx -l pl.UTF-8
Sterownik Open-MX dla Linuksa.

%prep
%setup -q

%build
%configure \
	--disable-debug \
	%{!?with_kernel:--disable-driver-build} \
	--disable-silent-rules \
	--with-linux=%{_kernelsrcdir} \
	--with-linux-build=%{_kernelsrcdir} \
	--with-linux-release=%{_kernel_ver}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	installmoddir=/lib/modules/%{_kernel_ver}/misc

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/omx_check
%attr(755,root,root) %{_bindir}/omx_counters
%attr(755,root,root) %{_bindir}/omx_endpoint_info
%attr(755,root,root) %{_bindir}/omx_hostname
%attr(755,root,root) %{_bindir}/omx_info
%attr(755,root,root) %{_bindir}/omx_init_peers
%attr(755,root,root) %{_bindir}/omx_prepare_binding
%attr(755,root,root) %{_bindir}/omxoed
%attr(755,root,root) %{_sbindir}/omx_init
%attr(755,root,root) %{_sbindir}/omx_local_install
%dir %{_sysconfdir}/open-mx
%{_sysconfdir}/open-mx/10-open-mx.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/open-mx/open-mx.conf
%{_mandir}/man1/omx_counters.1*
%{_mandir}/man1/omx_endpoint_info.1*
%{_mandir}/man1/omx_hostname.1*
%{_mandir}/man1/omx_info.1*
%{_mandir}/man1/omx_init_peers.1*
%{_mandir}/man1/omx_perf.1*
%{_mandir}/man1/omx_prepare_binding.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README REPORTING-BUGS TODO
%attr(755,root,root) %{_libdir}/libopen-mx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopen-mx.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopen-mx.so
# compatibility symlink
%attr(755,root,root) %{_libdir}/libmyriexpress.so
%{_includedir}/mx_internals
%{_includedir}/mx_extensions.h
%{_includedir}/mx_io.h
%{_includedir}/mx_raw.h
%{_includedir}/myriexpress.h
%{_includedir}/open-mx.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libopen-mx.a
# compatibility symlink
%{_libdir}/libmyriexpress.a

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-open-mx
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/open-mx.ko*
%endif
