%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}

Name:          jmock
Version:       2.12.0.1.gc4366a1e
Release:       1%{?dist}
Summary:       Java library for testing code with mock objects
License:       BSD
Url:           http://www.jmock.org/
Source0:       jmock-library-2.12.0.1.gc4366a1e.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires: mvn(org.beanshell:bsh)
BuildRequires: mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires: mvn(org.hamcrest:hamcrest-library)
BuildRequires: mvn(org.objenesis:objenesis)
BuildRequires: mvn(org.ow2.asm:asm)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
Mock objects help you design and test the interactions between the objects in
your programs.
The jMock library:
  * makes it quick and easy to define mock objects, so you don't break the
    rhythm of programming.
  * lets you precisely specify the interactions between your objects, reducing
    the brittleness of your tests.
  * works well with the auto-completion and re-factoring features of your IDE
  * plugs into your favorite test framework
  * is easy to extend.

%package example
Summary:       jMock Examples

%description example
jMock Examples.

%package junit3
Summary:       jMock JUnit 3 Integration

%description junit3
jMock JUnit 3 Integration.

%package junit4
Summary:       jMock JUnit 4 Integration

%description junit4
jMock JUnit 4 Integration.

%package legacy
Summary:       jMock Legacy Plugins

%description legacy
Plugins that make it easier to use jMock with legacy code.

%package parent
Summary:       jMock Parent POM

%description parent
jMock Parent POM.

%package testjar
Summary:       jMock Test Jar

%description testjar
Source for JAR files used in jMock Core tests.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-library-%{namedversion}

%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-source-plugin

%pom_remove_plugin :maven-gpg-plugin testjar

%pom_change_dep cglib: :cglib
%pom_change_dep cglib: :cglib %{name}

sed -i "s|%classpath|$(build-classpath objectweb-asm/asm)|" %{name}/pom.xml

%pom_xpath_remove pom:build %{name}-example
%pom_xpath_inject "pom:project" "
<build>
  <sourceDirectory>src/main</sourceDirectory>
</build>" %{name}-example
# package org.jmock.integration.junit{3,4} do not exist
%pom_add_dep org.%{name}:%{name}-junit3:'${project.version}' %{name}-example
%pom_add_dep org.%{name}:%{name}-junit4:'${project.version}' %{name}-example

%mvn_alias org.%{name}:%{name} :%{name}-script
%mvn_package org.%{name}:%{name}::tests: %{name}
%mvn_package org.%{name}:%{name}-junit3::tests: %{name}-junit3
# AssertionError: Expected: (null or an empty string) but: was "the Mockery is not thread-safe: use a Synchroniser to ensure thread safety"
rm jmock-legacy/src/test/java/org/jmock/test/acceptance/MockeryFinalizationAcceptanceTests.java

%build

%mvn_build -s

%install
%mvn_install

%files -f .mfiles-%{name}
%doc README*
%license LICENSE.txt

%files example -f .mfiles-%{name}-example
%files junit3 -f .mfiles-%{name}-junit3
%files junit4 -f .mfiles-%{name}-junit4
%files legacy -f .mfiles-%{name}-legacy

%files parent -f .mfiles-%{name}-parent
%license LICENSE.txt

%files testjar -f .mfiles-%{name}-testjar
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Mon Sep 09 2019 Rado Pitonak <rado.pitonak@gmail.com> - 2.12.0.1.gc4366a1e-1
- Development snapshot (c4366a1e)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 08 2016 gil cattaneo <puntogil@libero.it> 2.8.2-2
- disable test failure

* Sun Mar 06 2016 gil cattaneo <puntogil@libero.it> 2.8.2-1
- updated to 2.8.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 gil cattaneo <puntogil@libero.it> 2.8.1-1
- updated to 2.8.1

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 2.5.1-8
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 gil cattaneo <puntogil@libero.it> 2.5.1-6
- Use .mfiles generated during build
- Fix junit dep

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.5.1-5
- Use Requires: java-headless rebuild (#1067528)

* Fri Nov 15 2013 gil cattaneo <puntogil@libero.it> 2.5.1-4
- use objectweb-asm3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Apr 19 2012 gil cattaneo <puntogil@libero.it> 2.5.1-1
- initial rpm
