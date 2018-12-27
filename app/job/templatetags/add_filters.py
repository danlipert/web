from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    filters = request.GET.copy()
    filters.update(kwargs)
    filters['page'] = kwargs['page']
    return filters.urlencode()
