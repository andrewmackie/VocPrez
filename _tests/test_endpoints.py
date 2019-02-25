import requests
import json
import re

BASE_URLS = [
    'http://localhost:5000',
    # 'http://vocabs.gsq.cat'
]

N_TRIPLES_PATTERN = r'(_:(.+)|<.+>) (_:(.+)|<.+>) ("(.+)"@en)|(_:(.+)|(".+"\^\^)?<.+>) .'


#
# -- Test static pages -------------------------------------------------------------------------------------------------
#
def test_index_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL).content.decode('utf-8')
        assert '<h1>System Home</h1>' in content, BASE_URL


def test_about_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/about').content.decode('utf-8')
        assert '<p>A read-only web delivery system for Simple Knowledge Organization System (SKOS)-formulated RDF ' \
               'vocabularies.</p>' in content, BASE_URL


#
# -- Test vocabulary register ------------------------------------------------------------------------------------------
#

def test_vocabulary_register_ckan_view_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=ckan&_format=application/json&uri=' + BASE_URL
                               + '/vocabulary/').content.decode('utf-8')
        content = json.loads(content)
        assert 'head' and 'results' in content, BASE_URL
        assert 's' and 'pl' in content['head']['vars'], BASE_URL


def test_vocabulary_register_reg_view_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/').content.decode('utf-8')
        assert 'Search <em>Vocabularies:</em><br>' in content, BASE_URL


def test_vocabulary_register_reg_view_turtle():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=text/turtle&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        assert """@prefix ereg: <https://promsns.org/def/eregistry#> .
@prefix ldp: <http://www.w3.org/ns/ldp#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix xhv: <https://www.w3.org/1999/xhtml/vocab#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""" in content, BASE_URL


def test_vocabulary_register_reg_view_xml():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=application/rdf+xml&uri=' +
                               BASE_URL + '/vocabulary/').content.decode('utf-8')
        assert """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:ldp="http://www.w3.org/ns/ldp#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
   xmlns:reg="http://purl.org/linked-data/registry#"
   xmlns:xhv="https://www.w3.org/1999/xhtml/vocab#"
>""" in content, BASE_URL


def test_vocabulary_register_reg_view_app_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=application/json&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        content = json.loads(content)
        assert 'uri' and 'label' and 'comment' and 'contained_item_classes' and 'default_view' and 'register_items' \
               and 'views' in content, BASE_URL


def test_vocabulary_register_reg_view_ld_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=application/ld+json&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        content = json.loads(content)
        assert '@id' in content[0].keys(), BASE_URL


def test_vocabulary_register_reg_view_text_n3():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=text/n3&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
    assert """@prefix ereg: <https://promsns.org/def/eregistry#> .
@prefix ldp: <http://www.w3.org/ns/ldp#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix xhv: <https://www.w3.org/1999/xhtml/vocab#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""" in content, BASE_URL


def test_vocabulary_register_reg_view_app_n3():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?vocab_id=&_view=reg&_format=application/n-triples&uri=' +
                               BASE_URL + '/vocabulary/').content.decode('utf-8')
        content = content.split('\n')
        for line in content:
            line = line.strip()
            if line != '':
                result = re.search(N_TRIPLES_PATTERN, line)
                assert result is not None, 'URL: {} \n\nLine: {}'.format(BASE_URL, line)


def test_vocabulary_register_alternates_view_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates').content.decode('utf-8')
        assert '<td><a href="https://promsns.org/def/alt">https://promsns.org/def/alt</a></td>' in content
        assert '<h1>Alternates View</h1>' in content, BASE_URL


def test_vocabulary_register_alternates_view_app_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=application/json&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        content = json.loads(content)
        assert content['uri'] == BASE_URL + '/vocabulary/'
        assert content['default_view'] == 'reg'
        assert 'ckan' and 'reg' and 'alternates' in content['views'], BASE_URL


def test_vocabulary_register_alternates_view_turtle():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=text/turtle&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        assert """@prefix alt: <http://promsns.org/def/alt#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix prof: <https://w3c.github.io/dxwg/profiledesc#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""" in content, BASE_URL


def test_vocabulary_register_alternates_view_xml():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=application/rdf+xml&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        assert """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:alt="http://promsns.org/def/alt#"
   xmlns:dct="http://purl.org/dc/terms/"
   xmlns:prof="https://w3c.github.io/dxwg/profiledesc#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>""" in content, BASE_URL


def test_vocabulary_register_alternates_view_ld_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=application/ld+json&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        content = json.loads(content)
        assert '@id' in content[0].keys(), BASE_URL


def test_vocabulary_register_alternates_view_text_n3():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=text/n3&uri=' + BASE_URL +
                               '/vocabulary/').content.decode('utf-8')
        assert """@prefix alt: <http://promsns.org/def/alt#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix prof: <https://w3c.github.io/dxwg/profiledesc#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .""" in content, BASE_URL


def test_vocabulary_register_alternates_view_app_n_triples():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/?_view=alternates&_format=application/n-triples&uri=' + BASE_URL
                               + '/vocabulary/').content.decode('utf-8')
        content = content.split('\n')
        for line in content:
            line = line.strip()
            if line != '':
                result = re.search(N_TRIPLES_PATTERN, line)
                assert result is not None, 'URL: {} \n\nLine: {}'.format(BASE_URL, line)


#
# -- Test Vocabulary Instance (File Source) ----------------------------------------------------------------------------
#

def test_file_vocabulary_instance_dcat_view_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=text/html&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype')\
            .content.decode('utf-8')

        # Title
        assert '<h1>Vocabulary: Contact Type</h1>' in content, BASE_URL

        # URI
        assert '<a href="http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype">' \
               'http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype</a>' in content, BASE_URL

        # Description
        assert '<td>This scheme describes the concept space for Contact Type concepts, as defined by the IUGS ' \
               'Commission for Geoscience Information (CGI) Geoscience Terminology Working Group. By extension, it ' \
               'includes all concepts in this conceptScheme, as well as concepts in any previous versions of the ' \
               'scheme. Designed for use in the contactType property in GeoSciML Contact elements.</td>' \
               in content, BASE_URL

        # Creator
        assert '<td><a href="http://editor.vocabs.ands.org.au/user/CGI-Concept-Definition-Task-Group">' \
               'CGI-Concept-Definition-Task-Group</a></td>' in content, BASE_URL

        # Version
        assert """<tr>
        <th>Version Info:</th><td>v0.1</td>
    </tr>""" in content, BASE_URL

        # Top Concepts
        assert """<tr>
        <th>Top Concepts:</th>
        <td>
            
                <a href="/object?vocab_id=contact_type&uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/contact">contact</a><br />
            
        </td>
    </tr>""" in content, BASE_URL

        # Concept Hierarchy
        assert """<td>
                <ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/contact">contact</a> (1)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/chronostratigraphic_zone_contact">chronostratigraphic-zone contact</a> (2)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/faulted_contact">faulted contact</a> (2)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/geologic_province_contact">geologic province contact</a> (2)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/geophysical_contact">geophysical contact</a> (2)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/conductivity_contact">conductivity contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/density_contact">density contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/magnetic_contact">magnetic contact</a> (3)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/magnetic_polarity_contact">magnetic polarity contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/magnetic_susceptiblity_contact">magnetic susceptiblity contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/magnetization_contact">magnetization contact</a> (4)</li>
</ul>
</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/radiometric_contact">radiometric contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/seismic_contact">seismic contact</a> (3)</li>
</ul>
</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/glacial_stationary_line">glacial stationary line</a> (2)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/lithogenetic_contact">lithogenetic contact</a> (2)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/deformation_zone_contact">deformation zone contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/depositional_contact">depositional contact</a> (3)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/conformable_contact">conformable contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/unconformable_contact">unconformable contact</a> (4)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/angular_unconformable_contact">angular unconformable contact</a> (5)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/buttress_unconformity">buttress unconformity</a> (5)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/disconformable_contact">disconformable contact</a> (5)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/nonconformable_contact">nonconformable contact</a> (5)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/paraconformable_contact">paraconformable contact</a> (5)</li>
</ul>
</li>
</ul>
</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/igneous_intrusive_contact">igneous intrusive contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/igneous_phase_contact">igneous phase contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/impact_structure_boundary">impact structure boundary</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/metamorphic_contact">metamorphic contact</a> (3)<ul>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/alteration_facies_contact">alteration facies contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/metamorphic_facies_contact">metamorphic facies contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/metasomatic_facies_contact">metasomatic facies contact</a> (4)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/mineralisation_assemblage_contact">mineralisation assemblage contact</a> (4)</li>
</ul>
</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/sedimentary_facies_contact">sedimentary facies contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/sedimentary_intrusive_contact">sedimentary intrusive contact</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/volcanic_subsidence_zone_boundary">volcanic subsidence zone boundary</a> (3)</li>
<li><a href="{0}/object?vocab_id=contact_type&amp;uri=http%3A//resource.geosciml.org/classifier/cgi/contacttype/weathering_contact">weathering contact</a> (3)</li>
</ul>
</li>
</ul>
</li>
</ul>
        </td>""".format(BASE_URL) in content, BASE_URL


def test_file_vocabulary_instance_dcat_view_app_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=application/json&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype')\
            .content.decode('utf-8')
        assert """[
  {
    "@id": "http://resource.geosciml.org/classifier/cgi/contacttype/contact",
    "http://www.w3.org/2004/02/skos/core#prefLabel": [
      {
        "@value": "contact"
      }
    ]
  },
  {
    "@id": "http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype",
    "@type": [
      "https://www.w3.org/ns/dcat#Dataset"
    ],
    "http://purl.org/dc/terms/creator": [
      {
        "@id": "http://editor.vocabs.ands.org.au/user/CGI-Concept-Definition-Task-Group"
      }
    ],
    "http://purl.org/dc/terms/description": [
      {
        "@value": "This scheme describes the concept space for Contact Type concepts, as defined by the IUGS Commission for Geoscience Information (CGI) Geoscience Terminology Working Group. By extension, it includes all concepts in this conceptScheme, as well as concepts in any previous versions of the scheme. Designed for use in the contactType property in GeoSciML Contact elements."
      }
    ],
    "http://purl.org/dc/terms/title": [
      {
        "@value": "Contact Type"
      }
    ],
    "http://www.w3.org/2002/07/owl#versionInfo": [
      {
        "@value": "v0.1"
      }
    ],
    "http://www.w3.org/2004/02/skos/core#hasTopConcept": [
      {
        "@id": "http://resource.geosciml.org/classifier/cgi/contacttype/contact"
      }
    ]
  }
]""" in content, BASE_URL


def test_file_vocabulary_instance_dcat_view_turtle():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=text/turtle&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype')\
            .content.decode('utf-8')
        assert """@prefix dcat: <https://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype> a dcat:Dataset ;
    dct:creator <http://editor.vocabs.ands.org.au/user/CGI-Concept-Definition-Task-Group> ;
    dct:description "This scheme describes the concept space for Contact Type concepts, as defined by the IUGS Commission for Geoscience Information (CGI) Geoscience Terminology Working Group. By extension, it includes all concepts in this conceptScheme, as well as concepts in any previous versions of the scheme. Designed for use in the contactType property in GeoSciML Contact elements."@en ;
    dct:title "Contact Type"@en ;
    owl:versionInfo "v0.1"^^xsd:string ;
    skos:hasTopConcept <http://resource.geosciml.org/classifier/cgi/contacttype/contact> .

<http://resource.geosciml.org/classifier/cgi/contacttype/contact> skos:prefLabel "contact"^^xsd:string .
""" in content, BASE_URL


def test_file_vocabulary_instance_dcat_view_xml():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=application/rdf+xml&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype')\
            .content.decode('utf-8')
        assert """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:dct="http://purl.org/dc/terms/"
   xmlns:owl="http://www.w3.org/2002/07/owl#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:skos="http://www.w3.org/2004/02/skos/core#"
>""" in content, BASE_URL


def test_file_vocabulary_instance_dcat_view_ld_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=application/ld+json&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype')\
            .content.decode('utf-8')
        content = json.loads(content)
        assert content[0]['@id'] == "http://resource.geosciml.org/classifier/cgi/contacttype/contact", BASE_URL
        assert content[0]["http://www.w3.org/2004/02/skos/core#prefLabel"][0]['@value'] == 'contact', BASE_URL


def test_file_vocabulary_instance_dcat_view_turtle():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=text/n3&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype') \
            .content.decode('utf-8')
        assert """@prefix dcat: <https://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype> a dcat:Dataset ;
    dct:creator <http://editor.vocabs.ands.org.au/user/CGI-Concept-Definition-Task-Group> ;
    dct:description "This scheme describes the concept space for Contact Type concepts, as defined by the IUGS Commission for Geoscience Information (CGI) Geoscience Terminology Working Group. By extension, it includes all concepts in this conceptScheme, as well as concepts in any previous versions of the scheme. Designed for use in the contactType property in GeoSciML Contact elements."@en ;
    dct:title "Contact Type"@en ;
    owl:versionInfo "v0.1"^^xsd:string ;
    skos:hasTopConcept <http://resource.geosciml.org/classifier/cgi/contacttype/contact> .

<http://resource.geosciml.org/classifier/cgi/contacttype/contact> skos:prefLabel "contact"^^xsd:string .
""" in content, BASE_URL


def test_file_vocabulary_instance_dcat_view_app_n3():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=dcat&_format=application/n-triples&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype') \
            .content.decode('utf-8')
        content = content.split('\n')
        for line in content:
            line = line.strip()
            if line != '':
                result = re.search(N_TRIPLES_PATTERN, line)
                assert result is not None, 'URL: {} \n\nLine: {}'.format(BASE_URL, line)


def test_file_vocabulary_instance_alternates_view_html():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=alternates&_format=text/html&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype') \
            .content.decode('utf-8')
        assert """<h1>Alternates View</h1>
        <h2>Instance <a href="http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype">Contact Type</a></h2>""" \
               in content, BASE_URL


def test_file_vocabulary_instance_alternates_view_app_json():
    for BASE_URL in BASE_URLS:
        content = requests.get(BASE_URL + '/vocabulary/contact_type?_view=alternates&_format=application/json&uri='
                                          'http%3A//resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype') \
            .content.decode('utf-8')
        content = json.loads(content)
        assert content['uri'] == "http://resource.geosciml.org/classifierscheme/cgi/2016.01/contacttype"
        assert content['views'] == ["dcat", "alternates"]
        assert content['default_view'] == 'dcat'


