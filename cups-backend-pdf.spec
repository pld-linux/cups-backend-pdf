#
#TODO - add contrib dir

Summary:	CUPS-PDF driver
Summary(pl.UTF-8):	Sterownik CUPS-PDF
Name:		cups-pdf
Version:	2.4.7
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://www.cups-pdf.de/src/%{name}_%{version}.tar.gz
# Source0-md5:	46f73553336842dd67521da117bfc67e
URL:		http://www.cups-pdf.de/
BuildRequires:	cups-devel
Requires:	cups
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _libdir         %(cups-config --serverbin 2>/dev/null)

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

install src/cups-pdf $RPM_BUILD_ROOT%{_libdir}/backend
install extra/cups-pdf.conf  $RPM_BUILD_ROOT%{_sysconfdir}/cups
install extra/CUPS-PDF.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service cups restart "cups daemon"

%postun
%service cups restart "cups daemon"

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/%{name}.conf
%attr(700,root,root) %{_libdir}/backend/%{name}
%{_datadir}/cups/model/CUPS-PDF.ppd
%dir %{_var}/spool/%{name}
