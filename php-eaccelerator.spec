#
%define		pkgname		eaccelerator
Summary:	eAccelerator module for PHP
Summary(pl.UTF-8):	Moduł eAccelerator dla PHP
Name:		php-%{pkgname}
Version:	0.9.6.1
Release:	6
License:	GPL
Group:		Libraries
Source0:	http://bart.eaccelerator.net/source/%{version}/%{pkgname}-%{version}.tar.bz2
# Source0-md5:	32ccd838e06ef5613c2610c1c65ed228
Source1:	%{pkgname}.ini
URL:		http://eaccelerator.net/
BuildRequires:	php-devel >= 3:5.1.0
BuildRequires:	rpmbuild(macros) >= 1.344
%requires_eq	php-common
%{?requires_php_extension}
Requires:	php-common >= 4:5.1.0
Requires:	php-session
Requires:	php-zlib
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{pkgname}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

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
Summary(pl.UTF-8):	Interfejs WWW dla PHP Acceleratora
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	webapps
Requires:	webserver(php)

%description webinterface
PHP Accelerator can be managed through web interface script
control.php and dasm.php (which requires disassembler and tokenizer).
For security reasons it is recommended to restrict the usage of this
script by your local IP and setup password based access.

More information you can find at %{url}.

%description webinterface -l pl.UTF-8
PHP Accelerator może być sterowany ze strony internetowej z
wykorzystaniem skryptów control.php i dasm.php (który wymaga modułu
obsługującego disassembler i tokenizer). Z powodów bezpieczeństwa
zalecane jest, aby ograniczyć korzystanie ze skryptu do lokalnego
adresu i ustawić autoryzację hasłem.

Więcej informacji można znaleźć pod %{url}.

%prep
%setup -q -n %{pkgname}-%{version}

cat > apache.conf <<EOF
Alias /%{_webapp} %{_appdir}
<Directory %{_appdir}/>
	Order allow,deny
	Allow from 127.0.0.1
</Directory>
EOF

%build
phpize
%configure \
	--enable-eaccelerator=shared \
	--with-eaccelerator-userid=http \
	--without-eaccelerator-use-inode \
	--with-php-config=%{_bindir}/php-config \
	%{?debug:--with-eaccelerator-debug}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{_bindir},%{php_sysconfdir}/conf.d,/var/cache/%{pkgname},%{_sysconfdir},%{_appdir},/etc/tmpwatch}

install modules/eaccelerator.so $RPM_BUILD_ROOT%{php_extensiondir}
install %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{pkgname}.ini

cp -a {PHP_Highlight,control,dasm}.php $RPM_BUILD_ROOT%{_appdir}
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

echo "/var/cache/%{pkgname} 720" > $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin webinterface -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun webinterface -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin webinterface -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun webinterface -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -rf /var/cache/%{pkgname}/*
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README bugreport.php doc/php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{pkgname}.ini
%config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(755,root,root) %{php_extensiondir}/eaccelerator.so
%attr(770,root,http) /var/cache/%{pkgname}

%files webinterface
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_appdir}
%{_appdir}/PHP_Highlight.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/control.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/dasm.php
