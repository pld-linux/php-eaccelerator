%define		modname		eaccelerator
%define		php_name	php%{?php_suffix}
Summary:	eAccelerator module for PHP
Summary(pl.UTF-8):	Moduł eAccelerator dla PHP
Name:		%{php_name}-%{modname}
Version:	0.9.6.1
Release:	32
License:	GPL
Group:		Libraries
Source0:	http://bart.eaccelerator.net/source/%{version}/%{modname}-%{version}.tar.bz2
# Source0-md5:	32ccd838e06ef5613c2610c1c65ed228
Source1:	%{modname}.ini
Source2:	apache.conf
URL:		http://www.eaccelerator.net/
BuildRequires:	%{php_name}-devel >= 3:5.1.0
BuildRequires:	rpmbuild(macros) >= 1.344
%requires_eq	%{php_name}-common
%{?requires_php_extension}
Requires:	%{php_name}-session
Requires:	%{php_name}-zlib
Obsoletes:	php-eaccelerator < 0.9.6.1-30
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{modname}
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
Requires:	%{name} = %{version}-%{release}
Requires:	webapps
Requires:	webserver(php)
Obsoletes:	php-eaccelerator-webinterface < 0.9.6.1-30
BuildArch:	noarch

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
%setup -q -n %{modname}-%{version}

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
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{_bindir},%{php_sysconfdir}/conf.d,/var/cache/%{modname},%{_sysconfdir},%{_appdir},/etc/tmpwatch}

install -p modules/eaccelerator.so $RPM_BUILD_ROOT%{php_extensiondir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

cp -a {PHP_Highlight,control,dasm}.php $RPM_BUILD_ROOT%{_appdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

echo "/var/cache/%{modname} 720" > $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

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
%banner %{name} <<EOF
+-------------------------------------------------------+
|                 !!! Attention !!!                     |
|                                                       |
| For disk cache users (using eaccelerator.shm_only=0): |
|                                                       |
| Please remember to empty your eAccelerator disk cache |
| when upgrading, otherwise things will break!          |
+-------------------------------------------------------+
EOF

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -rf /var/cache/%{modname}/*
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README bugreport.php doc/php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%attr(755,root,root) %{php_extensiondir}/eaccelerator.so
%attr(770,root,http) /var/cache/%{modname}

%files webinterface
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_appdir}
%{_appdir}/PHP_Highlight.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/control.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/dasm.php
