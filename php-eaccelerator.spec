# TODO:
# - move php files to webapps framework
#
%define		_name		eaccelerator
%define		_pkgname	eaccelerator
Summary:	eAccelerator module for PHP
Summary(pl.UTF-8):   Moduł eAccelerator dla PHP
Name:		php-%{_name}
Version:	0.9.5
Release:	5
Epoch:		0
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}.tar.bz2
# Source0-md5:	dad54af67488b83a2af6e30f661f613b
Source1:	%{_name}.ini
Patch0:		%{name}-php5.2.patch
URL:		http://eaccelerator.net/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%requires_eq	php-common
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Requires:	php(zlib)
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eAccelerator is a further development from mmcache PHP Accelerator &
Encoder. It increases performance of PHP scripts by caching them in
compiled state, so that the overhead of compiling is almost completely
eliminated.

%description -l pl.UTF-8
eAccelerator to dalsze stadium rozwoju akceleratora i kodera PHP
mmcache. Zwiększa wydajność skryptów PHP poprzez zapamiętywanie ich w
postaci skompilowanej, dzięki czemu narzut potrzebny na kompilację
jest prawie całkowicie wyeliminowany.

%package webinterface
Summary:	WEB interface for PHP Accelerator
Summary(pl.UTF-8):   Interfejs WWW dla PHP Acceleratora
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description webinterface
PHP Accelerator can be managed through web interface script
eaccelerator.php. So you need to put this file on your web site. For
security reasons it is recommended to restrict the usage of this
script by your local IP and setup password based access.

More information you can find at %{url}.

%description webinterface -l pl.UTF-8
PHP Accelerator może być sterowany ze strony internetowej z
wykorzystaniem skryptu eaccelerator.php. Jedyne co trzeba zrobić, to
umieścić plik we właściwym miejscu na stronie internetowej. Z powodów
bezpieczeństwa zalecane jest, aby ograniczyć korzystanie ze skryptu do
lokalnego adresu i ustawić autoryzację hasłem.

Więcej informacji można znaleźć pod %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}
%patch0 -p1

%build
phpize
%configure \
	--enable-eaccelerator=shared \
	--with-eaccelerator-shared-memory \
	--with-eaccelerator-sessions \
	--with-eaccelerator-content-caching \
	--with-eaccelerator-userid=http \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{_bindir},%{php_sysconfdir}/conf.d,/var/cache/%{_name},/etc/tmpwatch}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{php_extensiondir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_name}.ini

install -d $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator
cp -a doc/php/* $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator

echo "/var/cache/%{_name} 720" > $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -rf /var/cache/%{_name}/*
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_name}.ini
%config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(755,root,root) %{php_extensiondir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
%attr(770,root,http) /var/cache/%{_name}

%files webinterface
%defattr(644,root,root,755)
/home/services/httpd/html/eaccelerator
