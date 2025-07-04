from django.db import models
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def paginate_queryset(queryset, request):
    page = request.query_params.get("page", 1)
    page_size = request.query_params.get("page_size", 10)
    try:
        page = int(page)
        page_size = int(page_size)
    except ValueError:
        page = 1
        page_size = 10

    paginator = Paginator(queryset, page_size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = []

    pagination_data = {
        "total": paginator.count,
        "page": page,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
        "has_next": objects.has_next() if objects else False,
        "has_previous": objects.has_previous() if objects else False,
    }
    return objects, pagination_data