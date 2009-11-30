# TODO
# - add contrib dir
Summary:	CUPS-PDF driver
Summary(pl.UTF-8):	Sterownik CUPS-PDF
Name:		cups-pdf
Version:	2.5.0
Release:	2
License:	GPL v2
Group:		Applications
Source0:	http://www.cups-pdf.de/src/%{name}_%{version}.tar.gz
# Source0-md5:	9194af099a8c0e9aa213505b29ec6818
URL:		http://www.cups-pdf.de/
BuildRequires:	cups-devel
Requires:	cups
Requires:	ghostscript
Conflicts:	ghostscript-esp < 8.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%(cups-config --serverbin 2>/dev/null)

%description
CUPS-PDF is designed to produce PDF files in a heterogeneous network
by providing a PDF printer on the central fileserver.

%description -l pl.UTF-8
CUPS-PDF służy do tworzenia plików PDF w środowisku heterogenicznym
poprzez udostępnienie drukarki PDF na centralnym serwerze plików.

%prep
%setup -q

%build
cd src
%{__cc} %{rpmldflags} %{rpmcflags} -o cups-pdf cups-pdf.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/backend,%{_sysconfdir}/cups,%{_datadir}/cups/model,%{_var}/spool/%{name}}
cp -a src/cups-pdf $RPM_BUILD_ROOT%{_libdir}/backend
cp -a extra/cups-pdf.conf  $RPM_BUILD_ROOT%{_sysconfdir}/cups
cp -a extra/CUPS-PDF.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q cups restart

%postun
if [ "$1" = 0 ]; then
	%service -q cups restart
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/%{name}.conf
%attr(700,root,root) %{_libdir}/backend/%{name}
%{_datadir}/cups/model/CUPS-PDF.ppd
%dir %{_var}/spool/%{name}
