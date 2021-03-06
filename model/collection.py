from pyldapi import Renderer, Profile
from flask import Response, render_template, g
from rdflib import Graph
from model.profiles import profile_skos


class Collection:
    def __init__(
        self, vocab, uri, label, comment, members,
    ):
        self.vocab = vocab
        self.uri = uri
        self.label = label
        self.comment = comment
        self.members = members


class CollectionRenderer(Renderer):
    def __init__(self, request, collection):
        self.profiles = self._add_skos_profile()
        self.navs = []  # TODO: add in other nav items for Collection

        self.collection = collection

        super().__init__(request, self.collection.uri, self.profiles, "skos")

    def _add_skos_profile(self):
        return {"skos": profile_skos}

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response
        elif self.profile == "skos":
            if self.mediatype in Renderer.RDF_MEDIA_TYPES:
                return self._render_skos_rdf()
            else:
                return self._render_skos_html()

    def _render_skos_rdf(self):
        # get Collection RDF
        # TODO: re-assemble RDF from Concept object
        g = Graph()

        # serialise in the appropriate RDF format
        if self.mediatype in ["application/rdf+json", "application/json"]:
            return g.serialize(format="json-ld")
        else:
            return g.serialize(format=self.mediatype)

    def _render_skos_html(self):
        _template_context = {
            "vocab_id": self.request.values.get("vocab_id"),
            "vocab_title": g.VOCABS[self.request.values.get("vocab_id")].title,
            "uri": self.instance_uri,
            "collection": self.collection,
            "navs": self.navs,
        }

        return Response(
            render_template("collection.html", **_template_context),
            headers=self.headers,
        )
