%define		php_name	php%{?php_suffix}
%define		modname	fam
%define		status		beta
Summary:	%{modname} - File Alteration Monitor Functions
Summary(pl.UTF-8):	%{modname} - monitor zmian w plikach
Name:		%{php_name}-pecl-%{modname}
Version:	5.0.1
Release:	3
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	2a5e358e7fec4f3b21610423a2652934
URL:		http://pecl.php.net/package/fam/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	fam-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-fam
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FAM monitors files and directories, notifying interested applications
of changes. A PHP script may specify a list of files for FAM to
monitor using the functions provided by this extension. The FAM
process is started when the first connection from any application to
it is opened. It exits after all connections to it have been closed.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
FAM monitoruje pliki i katalogi, informując aplikacje o występujących
w nich zmianach. Z poziomu skryptu PHP możliwe jest określenie listy
plików jakie FAM ma monitorować. Proces FAM jest uruchomiony gdy
pojawi się pierwsze połączenie, a kończony w momencie odłaczenia się
ostatniej aplikacji.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
