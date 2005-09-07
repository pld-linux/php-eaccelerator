%define		_name		eaccelerator
%define		_pkgname	eaccelerator
%define		php_ver		%(rpm -q --qf '%%{epoch}:%%{version}' php-devel)

Summary:	eAccelerator module for PHP
Summary(pl):	Modu³ eAccelerator dla PHP
Name:		php-%{_name}
Version:	0.9.3
Release:	1
Epoch:		0
License:	GPL
Vendor:		Turck Software
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	b17ddf953f18ee6df5c2c24ffccb37d9
URL:		http://eaccelerator.net/
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php = %{php_ver}
Requires:	php-zlib
Requires(post,preun):	php-common >= 3:5.0.0
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
eAccelerator is a further development from mmcache PHP Accelerator &
Encoder. It increases performance of PHP scripts by caching them in
compiled state, so that the overhead of compiling is almost completely
eliminated.

%description -l pl
eAccelerator to dalsze stadium rozwoju akceleratora i kodera PHP
mmcache. Zwiêksza wydajno¶æ skryptów PHP poprzez zapamiêtywanie ich w
postaci skompilowanej, dziêki czemu narzut potrzebny na kompilacjê
jest prawie ca³kowicie wyeliminowany.

%prep
%setup -q -n %{_pkgname}-%{version}

%build
phpize
%configure \
	--enable-mmcache=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}
install -d $RPM_BUILD_ROOT%{_bindir}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install eaccelerator %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove eaccelerator %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
