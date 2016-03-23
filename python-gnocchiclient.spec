%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             python-gnocchiclient
Version:          2.2.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Gnocchi

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.python.org/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}%{?milestone}.tar.gz

BuildArch:        noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr

Requires:         python-babel >= 1.3
Requires:         python-cliff >= 1.14.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneauth1 >= 1.0.0
Requires:         python-six >= 1.9.0
Requires:         python-futurist


%description
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool.


%package doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool
(gnocchi).

This package contains auto-generated documentation.


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Remove bundled egg-info
rm -rf gnocchiclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo

%files
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{python2_sitelib}/gnocchiclient
%{python2_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 2.2.0-0.1
-  Rebuild for Mitaka 
