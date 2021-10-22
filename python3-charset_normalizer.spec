# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	charset_normalizer
Summary:	The Real First Universal Charset Detector
Summary(pl.UTF-8):	Pierwszy prawdziwy uniwersalny wykrywacz kodowania znaków
Name:		python3-%{module}
Version:	2.0.7
Release:	3
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/9f/c5/334c019f92c26e59637bb42bd14a190428874b2b2de75a355da394cf16c1/charset-normalizer-%{version}.tar.gz
# Source0-md5:	b28e4463613ff3911d5a2dc62b96233f
URL:		https://github.com/ousret/charset_normalizer
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-recommonmark
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-pytest-cov
%endif
# when using /usr/bin/env or other in-place substitutions
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Real First Universal Charset Detector. Open, modern and actively
maintained alternative to Chardet.

%description -l pl.UTF-8
Pierwszy prawdziwy uniwersalny wykrywacz kodowania znaków. Otwarta,
noweczesna i aktywnie rozwijana alternatywa dla Chardet.

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

# fix #!%{_bindir}/env python -> #!%{_bindir}/python:
#%{__sed} -i -e '1s,^#!.*python3,#!%{__python3},' %{name}.py

%build
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
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
%doc docs/_build/html/*
%endif
