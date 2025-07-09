import hashlib
from django import template

register = template.Library()

@register.filter(name='make_hash')
def make_hash(value):
    """Hashes the input using SHA-256 as required by Meta Conversion API."""
    if value:
        return hashlib.sha256(value.strip().lower().encode()).hexdigest()
    return ""