#
#TODO - add contrib dir

Summary:	CUPS-PDF
Summary(pl.UTF-8):	CUPS-PDF
Name:		cups-pdf
Version:	2.4.6
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://www.cups-pdf.de/src/%{name}_%{version}.tar.gz
# Source0-md5:	610a2e1d9ecd27ab978efaa6d93ddba3
URL:		http://www.cups-pdf.de/
Requires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CUPS-PDF is designed to produce PDF files in a heterogeneous network
by providing a PDF printer on the central fileserver.

%prep
%setup -q

%build
cd src
%{__cc} -O9 -s -o cups-pdf cups-pdf.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/cups/backend,%{_sysconfdir}/cups,%{_datadir}/cups/model,%{_var}/spool/%{name}}

install src/cups-pdf $RPM_BUILD_ROOT%{_libdir}/cups/backend
install extra/cups-pdf.conf  $RPM_BUILD_ROOT%{_sysconfdir}/cups
install extra/PostscriptColor.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service cups restart "cups daemon"

%postun
%service cups restart "cups daemon"

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/cups/backend/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/%{name}.conf
%{_datadir}/cups/model/PostscriptColor.ppd
%dir %{_var}/spool/%{name}
