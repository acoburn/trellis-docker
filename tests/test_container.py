import pytest
import requests
from requests.utils import parse_header_links


def test_get_container(baseurl):
    r = requests.get(baseurl)

    assert 200 == r.status_code
    assert "text/turtle" == r.headers['content-type']
    links = parse_header_links(r.headers['link'])
    types = [l['url'] for l in links if (l['rel'] == 'type')]
    assert "http://www.w3.org/ns/ldp#BasicContainer" in types
    assert "http://www.w3.org/ns/ldp#Resource" in types

def test_get_json_ld(baseurl):
    r = requests.get(baseurl, headers={"accept": "application/ld+json"})
    assert 200 == r.status_code
    assert "application/ld+json" == r.headers['content-type']

def test_post_binary(baseurl):
    headers = {
            "content-type": "text/plain",
            "link": "<http://www.w3.org/ns/ldp#NonRDFSource>; rel='type'"}
    data = "A simple file."
    r = requests.post(baseurl, headers=headers, data=data)
    assert 201 == r.status_code
    location = r.headers['location']

    r = requests.get(location)
    assert 200 == r.status_code
    assert "text/plain" == r.headers['content-type']
    assert data == r.text

    r = requests.get(baseurl, headers={"accept":"application/ld+json"})
    d = r.json()
    assert location in d['contains']

def test_post_rdf(baseurl):
    headers = {
            "content-type": "text/turtle",
            "link": "<http://www.w3.org/ns/ldp#RDFSource>; rel='type'"}
    data = "<> a <http://example.com/TestResource> ."
    r = requests.post(baseurl, headers=headers, data=data)
    assert 201 == r.status_code
    location = r.headers['location']

    r = requests.get(location, headers={"accept":"application/ld+json"})
    assert 200 == r.status_code
    assert "application/ld+json" == r.headers['content-type']
    d = r.json()
    assert "http://example.com/TestResource" == d['@type']

    r = requests.get(baseurl, headers={"accept":"application/ld+json"})
    d = r.json()
    assert location in d['contains']


