# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section   free

Name:           smack
Version:        2.2.1
Release:        %mkrel 0.0.2
Epoch:          0
Summary:        Open Source XMPP (Jabber) client library

Group:          Development/Java
License:        Apache Software License 2.0
URL:            http://www.igniterealtime.org/projects/smack/index.jsp
Source0:        http://www.igniterealtime.org/downloads/download-landing.jsp?file=smack/smack_src_2_2_1.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-rpmbuild
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-contrib >= 0:1.0
BuildRequires:  junit >= 0:3.8.1
BuildRequires:  xpp3
BuildRequires:  jzlib
Requires:  xpp3

%description
Smack is an Open Source XMPP (Jabber) client library for instant 
messaging and presence. A pure Java library, it can be embedded 
into your applications to create anything from a full XMPP client 
to simple XMPP integrations such as sending notification messages.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        manual
Summary:        Documents for %{name}
Group:          Development/Java

%description    manual
%{summary}.


%prep
%setup -q -n %{name}-dev-%{version}
%remove_java_binaries

%build
pushd build
ln -sf $(build-classpath ant-contrib)
ln -sf $(build-classpath junit)
pushd merge
ln -sf $(build-classpath xpp3) xpp.jar
ln -sf $(build-classpath jzlib)
popd
popd
%ant -f build/build.xml jar javadoc jar-test

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 644 %{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 %{name}x.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}x-%{version}.jar

install -m 644 %{name}-test.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-test-%{version}.jar
install -m 644 %{name}x-debug.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}x-debug-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadocs
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr documentation/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
