Name: opflood
Version: 1.2
Release: 1%{?rel}
Summary: The script contains a minimum set of customers for PostgreSQL and Oracle. Designed for use SQL injection.

Group: Server Support
License: MIT
Vendor: Voskhod
Packager: Dmitriy Bulynenkov <d.bulynenkov@voskhod.ru>

BuildArch: noarch
BuildRequires: python

Source0: opflood.py
Source1: Install_requires.tar.gz

%description
%summary.

%prep
rm -rf %buildroot

%install
mkdir -p %buildroot/opt/opflood/archive
mkdir -p %buildroot/opt/opflood/log
cp -f %SOURCE0 %buildroot/opt/opflood/opflood.py
tar zxvf %SOURCE1 -C %buildroot/opt/opflood/archive


%files
%dir %attr(766, root, root) /opt/opflood
/opt/opflood/*
%attr(777, -, -) /opt/opflood/opflood.py

%post
ln -f /opt/opflood/opflood.py /usr/bin/opflood

%changelog
* Fri Aug 14 2015 Dmitriy Bulynenkov <d.bulynenkov@voskhod.ru>
- Initial RPM release