%define underscore_version 2_6_2

Name:           tinyxml
Version:        2.6.2
Release:        0
Summary:        A simple, small, C++ XML parser
Group:          System Environment/Libraries
License:        zlib
URL:            http://www.grinninglizard.com/tinyxml/
Source0:        %{name}_%{underscore_version}.tar.gz

%description
TinyXML is a simple, small, C++ XML parser that can be easily integrating
into other programs.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}


%build
# Not really designed to be build as lib, DYI
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
  g++ $RPM_OPT_FLAGS -fPIC -o $i.o -c $i
done
g++ $RPM_OPT_FLAGS -shared -o lib%{name}.so.0.%{version} \
   -Wl,-soname,lib%{name}.so.0 *.cpp.o


%install
rm -rf %{buildroot}/
# Not really designed to be build as lib, DYI
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}
install -m 755 lib%{name}.so.0.%{version} %{buildroot}/%{_libdir}
ln -s lib%{name}.so.0.%{version} %{buildroot}/%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0.%{version} %{buildroot}/%{_libdir}/lib%{name}.so
install -p -m 644 %{name}.h %{buildroot}/%{_includedir}


%clean
rm -rf %{buildroot}/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc changes.txt readme.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_includedir}/*
%{_libdir}/*.so