%define		_name		eaccelerator
%define		_pkgname	eaccelerator
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
%define		_rc		beta1

Summary:	eAccelerator module for PHP
Summary(pl):	Modu³ eAccelerator dla PHP
Name:		php-%{_name}
Version:	0.9.5
Release:	0.%{_rc}.1
Epoch:		0
License:	GPL
Vendor:		Turck Software
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}-%{_rc}.tar.bz2
# Source0-md5:	29f68a5975c1a09dbd72c9e8ddd534a7
Source1:	%{_name}.ini
URL:		http://eaccelerator.net/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%{?requires_php_extension}
%requires_eq	php-common
Requires:	%{_sysconfdir}/conf.d
Requires:	php-zlib
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package webinterface
Summary:	WEB interface for PHP Accelerator
Summary(pl):	Interfejs WWW dla PHP Acceleratora
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description webinterface
PHP Accelerator can be managed through web interface script
eaccelerator.php. So you need to put this file on your web site. For
security reasons it is recommended to restrict the usage of this
script by your local IP and setup password based access.

More information you can find at %{url}.

%description webinterface -l pl
PHP Accelerator mo¿e byæ sterowany ze strony internetowej z
wykorzystaniem skryptu eaccelerator.php. Jedyne co trzeba zrobiæ, to
umie¶ciæ plik we w³a¶ciwym miejscu na stronie internetowej. Z powodów
bezpieczeñstwa zalecane jest, aby ograniczyæ korzystanie ze skryptu do
lokalnego adresu i ustawiæ autoryzacjê has³em.

Wiêcej informacji mo¿na znale¼æ pod %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}-%{_rc}

%build
phpize
%configure \
	--enable-eaccelerator=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{extensionsdir},%{_bindir},%{_sysconfdir}/conf.d,/var/cache/%{_name}}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install ./eaccelerator_password.php $RPM_BUILD_ROOT%{_bindir}
install ./eaccelerator.php $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_name}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -f /var/cache/%{_name}/*
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
%attr(770,root,http) /var/cache/%{_name}

%files webinterface
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eaccelerator.php
%attr(755,root,root) %{_bindir}/eaccelerator_password.php
