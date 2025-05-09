# TODO
# - add contrib dir
# - spool & results in same dir is not good?
#   /var/spool/cups-pdf/SPOOL
Summary:	CUPS PDF driver
Summary(pl.UTF-8):	Sterownik CUPS-PDF
Name:		cups-backend-pdf
Version:	3.0.2
Release:	1
License:	GPL v2
Group:		Applications/Printing
Source0:	https://www.cups-pdf.de/src/cups-pdf_%{version}.tar.gz
# Source0-md5:	276402ca8d7ac1f249cdaf3c34bdfc51
URL:		https://www.cups-pdf.de/
BuildRequires:	cups-devel
Requires:	cups
Requires:	ghostscript
Obsoletes:	cups-pdf < 2.5.1
Conflicts:	ghostscript-esp < 8.15.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cupslibdir	%(cups-config --serverbin 2>/dev/null)

%description
CUPS-PDF is designed to produce PDF files in a heterogeneous network
by providing a PDF printer on the central fileserver.

%description -l pl.UTF-8
CUPS-PDF służy do tworzenia plików PDF w środowisku heterogenicznym
poprzez udostępnienie drukarki PDF na centralnym serwerze plików.

%prep
%setup -q -n cups-pdf-%{version}

%build
cd src
%{__cc} %{rpmldflags} %{rpmcflags} %{rpmcppflags} -o cups-pdf cups-pdf.c -lcups

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{cupslibdir}/backend,%{_sysconfdir}/cups,%{_datadir}/cups/model,%{_var}/spool/cups-pdf/SPOOL}
cp -a src/cups-pdf $RPM_BUILD_ROOT%{cupslibdir}/backend
cp -a extra/cups-pdf.conf  $RPM_BUILD_ROOT%{_sysconfdir}/cups
cp -a extra/*.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/cups-pdf.conf
%attr(700,root,root) %{cupslibdir}/backend/cups-pdf
%{_datadir}/cups/model/CUPS-PDF_noopt.ppd
%{_datadir}/cups/model/CUPS-PDF_opt.ppd
%dir %{_var}/spool/cups-pdf
%dir %attr(751,root,lp) %{_var}/spool/cups-pdf/SPOOL
