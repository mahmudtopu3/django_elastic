from elasticsearch_dsl import analyzer

from elasticsearch_dsl import __version__
__all__ = (
    'html_strip',
)

# The ``standard`` filter has been removed in Elasticsearch 7.x.
if __version__[0]>=7:
    _filters = ["lowercase", "stop", "snowball"]
else:
    _filters = ["standard", "lowercase", "stop", "snowball"]

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=_filters,
    char_filter=["html_strip"]
)