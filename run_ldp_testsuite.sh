#!/bin/sh

# Download ldp testsuite
wget --quiet https://www.trellisldp.org/ldp/ldp-testsuite.jar

# Create a basic container
curl -s http://127.0.0.1/ -XPOST -H"Slug: basic" -H"Link: <http://www.w3.org/ns/ldp#BasicContainer>; rel=\"type\"" -H"Content-Type: text/turtle" --data-binary @resources/basic.ttl
java -jar ldp-testsuite.jar --server http://127.0.0.1/basic --basic | grep -v DEBUG
mv report/ldp-testsuite-execution-report.html report/basic.html

# Create a direct container
curl -s http://127.0.0.1/ -XPOST -H"Slug: member_dc" -H"Link: <http://www.w3.org/ns/ldp#RDFSource>; rel=\"type\"" -H"Content-Type: text/turtle" --data-binary @resources/member.ttl
curl -s http://127.0.0.1/ -XPOST -H"Slug: direct" -H"Link: <http://www.w3.org/ns/ldp#DirectContainer>; rel=\"type\"" -H"Content-Type: text/turtle" --data-binary @resources/direct.ttl
java -jar ldp-testsuite.jar --server http://127.0.0.1/direct --direct | grep -v DEBUG
mv report/ldp-testsuite-execution-report.html report/direct.html

# Create an indirect container
curl -s http://127.0.0.1/ -XPOST -H"Slug: member_ic" -H"Link: <http://www.w3.org/ns/ldp#RDFSource>; rel=\"type\"" -H"Content-Type: text/turtle" --data-binary @resources/member.ttl
curl -s http://127.0.0.1/ -XPOST -H"Slug: indirect" -H"Link: <http://www.w3.org/ns/ldp#IndirectContainer>; rel=\"type\"" -H"Content-Type: text/turtle" --data-binary @resources/indirect.ttl
java -jar ldp-testsuite.jar --server http://127.0.0.1/indirect --indirect | grep -v DEBUG
mv report/ldp-testsuite-execution-report.html report/indirect.html

