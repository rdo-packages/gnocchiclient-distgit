%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc \
This is a client library for Gnocchi built on the Gnocchi API. It \
provides a Python API (the gnocchiclient module) and a command-line tool.

Name:             python-gnocchiclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Gnocchi

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch


%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python2-gnocchiclient}


BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-tools

Requires:         python-cliff >= 1.16.0
Requires:         python-osc-lib >= 1.7.0
Requires:         python-keystoneauth1 >= 2.0.0
Requires:         python-six >= 1.9.0
Requires:         python-futurist
Requires:         python-ujson
Requires:         python-pbr
Requires:         python-monotonic
Requires:         python-iso8601


%description -n python2-%{pypi_name}
%{common_desc}


%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-openstack-doc-tools
BuildRequires:    python-cliff
BuildRequires:    python-keystoneauth1
BuildRequires:    python-six
BuildRequires:    python-futurist
BuildRequires:    python-ujson
BuildRequires:    python-sphinx_rtd_theme
# test
BuildRequires:    python-babel

%description      doc
This is a client library for Gnocchi built on the Gnocchi API. It
provides a Python API (the gnocchiclient module) and a command-line tool
(gnocchi).

This package contains auto-generated documentation.

%package -n python2-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Gnocchi Tests
Requires:         python-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi

%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools
BuildRequires:    python3-tools

Requires:         python3-cliff >= 1.16.0
Requires:         python3-osc-lib >= 1.7.0
Requires:         python3-keystoneauth1 >= 2.0.0
Requires:         python3-six >= 1.9.0
Requires:         python3-futurist
Requires:         python3-ujson
Requires:         python3-pbr
Requires:         python3-monotonic
Requires:         python3-iso8601

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Gnocchi Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}

%endif

%description
%{common_desc}


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

# Remove bundled egg-info
rm -rf gnocchiclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/gnocchi %{buildroot}%{_bindir}/python3-gnocchi
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
install -m 755 -d %{buildroot}/%{_bindir}
pushd %{buildroot}%{_bindir}
for i in gnocchi-{2,%{?python2_shortver}}; do
    ln -s gnocchi $i
done
%if 0%{?with_python3}
for i in gnocchi-{3,%{?python3_shortver}}; do
    ln -s  python3-gnocchi $i
done
%endif
popd

# Some env variables required to successfully build our doc
export PATH=$PATH:%{buildroot}%{_bindir}
export PYTHONPATH=.
export LANG=en_US.utf8
python setup.py build_sphinx

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{_bindir}/gnocchi-2*
%{python2_sitelib}/gnocchiclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/gnocchiclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/gnocchiclient/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/python3-gnocchi
%{_bindir}/gnocchi-3*
%{python3_sitelib}/gnocchiclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/gnocchiclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/gnocchiclient/tests

%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html

%changelog
