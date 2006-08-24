# TODO:
# - move php files to webapps framework
#
%define		_name		eaccelerator
%define		_pkgname	eaccelerator
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
%define		_rc		rc1
%define		_rel		3
#
Summary:	eAccelerator module for PHP
Summary(pl):	Modu� eAccelerator dla PHP
Name:		php-%{_name}
Version:	0.9.5
Release:	0.%{_rc}.%{_rel}
Epoch:		0
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}-%{_rc}.tar.bz2
# Source0-md5:	5d03deb399f8f857d92dd092a2c69a87
Source1:	%{_name}.ini
URL:		http://eaccelerator.net/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%requires_eq	php-common
%{?requires_php_extension}
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
mmcache. Zwi�ksza wydajno�� skrypt�w PHP poprzez zapami�tywanie ich w
postaci skompilowanej, dzi�ki czemu narzut potrzebny na kompilacj�
jest prawie ca�kowicie wyeliminowany.

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
PHP Accelerator mo�e by� sterowany ze strony internetowej z
wykorzystaniem skryptu eaccelerator.php. Jedyne co trzeba zrobi�, to
umie�ci� plik we w�a�ciwym miejscu na stronie internetowej. Z powod�w
bezpiecze�stwa zalecane jest, aby ograniczy� korzystanie ze skryptu do
lokalnego adresu i ustawi� autoryzacj� has�em.

Wi�cej informacji mo�na znale�� pod %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}-%{_rc}

%build
phpize
%configure \
	--enable-eaccelerator=shared \
	--with-eaccelerator-userid=http \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{extensionsdir},%{_bindir},%{_sysconfdir}/conf.d,/var/cache/%{_name},/etc/tmpwatch}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_name}.ini

install -d $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator
cp -a doc/php/* $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator

echo "/var/cache/%{_name} 720" > $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

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
	rm -rf /var/cache/%{_name}/*
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
%attr(770,root,http) /var/cache/%{_name}

%files webinterface
%defattr(644,root,root,755)
/home/services/httpd/html/eaccelerator
