%define		_modname	fam
%define		_status		beta
Summary:	%{_modname} - File Alteration Monitor Functions
Summary(pl.UTF-8):	%{_modname} - monitor zmian w plikach
Name:		php-pecl-%{_modname}
Version:	5.0.1
Release:	2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	2a5e358e7fec4f3b21610423a2652934
URL:		http://pecl.php.net/package/fam/
BuildRequires:	fam-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-fam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAM monitors files and directories, notifying interested applications
of changes. A PHP script may specify a list of files for FAM to
monitor using the functions provided by this extension. The FAM
process is started when the first connection from any application to
it is opened. It exits after all connections to it have been closed.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
FAM monitoruje pliki i katalogi, informując aplikacje o występujących
w nich zmianach. Z poziomu skryptu PHP możliwe jest określenie listy
plików jakie FAM ma monitorować. Proces FAM jest uruchomiony gdy
pojawi się pierwsze połączenie, a kończony w momencie odłaczenia się
ostatniej aplikacji.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
