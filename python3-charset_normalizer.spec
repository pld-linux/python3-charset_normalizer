#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	charset_normalizer
Summary:	The Real First Universal Charset Detector
Summary(pl.UTF-8):	Pierwszy prawdziwy uniwersalny wykrywacz kodowania znaków
Name:		python3-%{module}
Version:	2.0.12
Release:	6
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/charset-normalizer/
Source0:	https://files.pythonhosted.org/packages/source/c/charset-normalizer/charset-normalizer-%{version}.tar.gz
# Source0-md5:	f6664e0e90dbb3cc9cfc154a980f9864
URL:		https://github.com/ousret/charset_normalizer
BuildRequires:	python3-modules >= 1:3.5.0
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-pytest-cov
%endif
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-recommonmark
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5.0
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
%setup -q -n charset-normalizer-%{version}

# broken, https://github.com/jawah/charset_normalizer/issues/167
%{__mv} tests/{,NOT-}test_logging.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest tests
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
%doc LICENSE README.md
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%attr(755,root,root) %{_bindir}/normalizer
%dir %{py3_sitescriptdir}/%{module}/assets
%{py3_sitescriptdir}/%{module}/assets/*.py
%{py3_sitescriptdir}/%{module}/assets/__pycache__
%dir %{py3_sitescriptdir}/%{module}/cli
%{py3_sitescriptdir}/%{module}/cli/*.py
%{py3_sitescriptdir}/%{module}/cli/__pycache__
%{py3_sitescriptdir}/%{module}/py.typed

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
