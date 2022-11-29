%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# NOTE(jpena): doc build fails with recent cliff versions, and hardcodes
# a call to unversioned python in
# https://github.com/gnocchixyz/python-gnocchiclient/blob/master/doc/source/conf.py#L54
%global with_doc 0

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python3-gnocchiclient}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}


BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-tools

Requires:         python3-cliff >= 2.10
Requires:         python3-keystoneauth1 >= 2.0.0
Requires:         python3-six >= 1.10.0
Requires:         python3-futurist
Requires:         python3-ujson
Requires:         python3-pbr
Requires:         python3-iso8601
Requires:         python3-dateutil
Requires:         python3-debtcollector
Requires:         python3-monotonic

%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

BuildRequires:    python3-sphinx
BuildRequires:    python3-cliff >= 2.10
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-six
BuildRequires:    python3-futurist
BuildRequires:    python3-ujson
BuildRequires:    python3-sphinx_rtd_theme
# test
BuildRequires:    python3-babel
# Runtime requirements needed during documentation build
BuildRequires:    python3-dateutil
BuildRequires:    python3-monotonic

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version}

2to3 --write --nobackups .

# Remove bundled egg-info
rm -rf gnocchiclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# Some env variables required to successfully build our doc
export PYTHONPATH=.
export LANG=en_US.utf8
%{__python3} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s gnocchi %{buildroot}%{_bindir}/gnocchi-3

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{_bindir}/gnocchi-3
%{python3_sitelib}/gnocchiclient
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%endif

%changelog
