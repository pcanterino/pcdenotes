from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
from markdown.extensions import Extension

register = template.Library()

# See https://python-markdown.github.io/change_log/release-3.0/#safe_mode-and-html_replacement_text-keywords-deprecated
class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')

@register.filter
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=[EscapeHtml(), 'nl2br'])