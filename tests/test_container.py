import unittest
import requests
from requests.utils import parse_header_links


class TestContainer(unittest.TestCase):

    ROOT = "http://localhost:8080/";

    def test_get_container(self):
        r = requests.get(self.ROOT)

        self.assertEqual(200, r.status_code)
        self.assertEqual("text/turtle", r.headers['content-type'])
        links = parse_header_links(r.headers['link'])
        types = [l['url'] for l in links if (l['rel'] == 'type')]
        self.assertTrue("http://www.w3.org/ns/ldp#BasicContainer" in types)
        self.assertTrue("http://www.w3.org/ns/ldp#Resource" in types)

    def test_get_json_ld(self):
        r = requests.get(self.ROOT, headers={"accept": "application/ld+json"})
        self.assertEqual(200, r.status_code)
        self.assertEqual("application/ld+json", r.headers['content-type'])

    def test_post_binary(self):
        headers = {
                "content-type": "text/plain",
                "link": "<http://www.w3.org/ns/ldp#NonRDFSource>; rel='type'"}
        data = "A simple file."
        r = requests.post(self.ROOT, headers=headers, data=data)
        self.assertEqual(201, r.status_code)
        location = r.headers['location']

        r = requests.get(location)
        self.assertEqual(200, r.status_code)
        self.assertEqual("text/plain", r.headers['content-type'])
        self.assertEqual(data, r.text)

        r = requests.get(self.ROOT, headers={"accept":"application/ld+json"})
        d = r.json()
        self.assertTrue(location in d['contains'])

    def test_post_rdf(self):
        headers = {
                "content-type": "text/turtle",
                "link": "<http://www.w3.org/ns/ldp#RDFSource>; rel='type'"}
        data = "<> a <http://example.com/TestResource> ."
        r = requests.post(self.ROOT, headers=headers, data=data)
        self.assertEqual(201, r.status_code)
        location = r.headers['location']

        r = requests.get(location, headers={"accept":"application/ld+json"})
        self.assertEqual(200, r.status_code)
        self.assertEqual("application/ld+json", r.headers['content-type'])
        d = r.json()
        self.assertEqual("http://example.com/TestResource", d['@type'])

        r = requests.get(self.ROOT, headers={"accept":"application/ld+json"})
        d = r.json()
        self.assertTrue(location in d['contains'])


