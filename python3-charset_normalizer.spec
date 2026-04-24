#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	charset_normalizer
Summary:	The Real First Universal Charset Detector
Summary(pl.UTF-8):	Pierwszy prawdziwy uniwersalny wykrywacz kodowania znaków
Name:		python3-%{module}
Version:	3.4.7
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/charset-normalizer/
Source0:	https://files.pythonhosted.org/packages/source/c/charset-normalizer/charset_normalizer-%{version}.tar.gz
# Source0-md5:	68805886064d248d2e5205fd11112d85
URL:		https://github.com/jawah/charset_normalizer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:68
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-pytest >= 7.4.4
%endif
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Real First Universal Charset Detector. Open, modern and actively
maintained alternative to Chardet.

%description -l pl.UTF-8
Pierwszy prawdziwy uniwersalny wykrywacz kodowania znaków. Otwarta,
nowoczesna i aktywnie rozwijana alternatywa dla Chardet.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o "pythonpath=$(pwd)/build-3/lib" tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md SECURITY.md
%attr(755,root,root) %{_bindir}/normalizer
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,community,user,*.html,*.js}
%endif
