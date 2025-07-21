#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	cookie
Summary:	HTTP cookie parsing and rendering
Summary(pl.UTF-8):	Analiza i renderowanie ciasteczek HTTP
Name:		ghc-%{pkgname}
Version:	0.4.5
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/cookie
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a3739514859a70325882534daeeddbe2
URL:		http://hackage.haskell.org/package/cookie
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10.2
BuildRequires:	ghc-data-default-class
BuildRequires:	ghc-deepseq
BuildRequires:	ghc-text >= 1.1
BuildRequires:	ghc-time >= 1.5
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-bytestring-prof >= 0.10.2
BuildRequires:	ghc-data-default-class-prof
BuildRequires:	ghc-deepseq-prof
BuildRequires:	ghc-text-prof >= 1.1
BuildRequires:	ghc-time-prof >= 1.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4
Requires:	ghc-bytestring >= 0.10.2
Requires:	ghc-data-default-class
Requires:	ghc-deepseq
Requires:	ghc-text >= 1.1
Requires:	ghc-time >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
HTTP cookie parsing and rendering.

%description -l pl.UTF-8
Analiza i renderowanie ciasteczek HTTP.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-bytestring-prof >= 0.10.2
Requires:	ghc-data-default-class-prof
Requires:	ghc-deepseq-prof
Requires:	ghc-text-prof >= 1.1
Requires:	ghc-time-prof >= 1.5

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build

runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Web
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Web/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Web/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Web/*.p_hi
%endif
