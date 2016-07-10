%global sname gnocchiclient
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-gnocchiclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Gnocchi

License:          ASL 2.0
URL:              https://bugs.launchpad.net/python-gnocchiclient
Source0:          http://tarballs.openstack.org/python-gnochhiclient/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

%description
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool.

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python2-gnocchiclient}

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr

Requires:         python-cliff >= 1.14.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneauth1 >= 1.0.0
Requires:         python-six >= 1.9.0
Requires:         python-futurist

%description -n python2-%{sname}
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python3-gnocchiclient}

BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr

Requires:         python3-cliff >= 1.14.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-serialization >= 1.4.0
Requires:         python3-oslo-utils >= 2.0.0
Requires:         python3-keystoneauth1 >= 1.0.0
Requires:         python3-six >= 1.9.0
Requires:         python3-futurist

%description -n python3-%{sname}
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool.
%endif

%package doc
Summary:          Documentation for OpenStack Gnocchi API Client

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool
(gnocchi).

This package contains auto-generated documentation.

%prep
%setup -q -n %{sname}-%{upstream_version}

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/gnocchi %{buildroot}%{_bindir}/gnocchi-%{python3_version}
ln -s ./gnocchi-%{python3_version} %{buildroot}%{_bindir}/gnocchi-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/gnocchiclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/gnocchi %{buildroot}%{_bindir}/gnocchi-%{python2_version}
ln -s ./gnocchi-%{python2_version} %{buildroot}%{_bindir}/gnocchi-2

ln -s ./gnocchi-2 %{buildroot}%{_bindir}/gnocchi
# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/gnocchiclient/tests


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/gnocchiclient
%{python2_sitelib}/*.egg-info
%{_bindir}/gnocchi
%{_bindir}/gnocchi-2
%{_bindir}/gnocchi-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/gnocchi-3
%{_bindir}/gnocchi-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
