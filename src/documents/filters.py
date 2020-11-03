from django_filters.rest_framework import BooleanFilter, FilterSet, Filter

from .models import Correspondent, Document, Tag, DocumentType, Log

CHAR_KWARGS = ["istartswith", "iendswith", "icontains", "iexact"]
ID_KWARGS = ["in", "exact"]
INT_KWARGS = ["exact", "gt", "gte", "lt", "lte"]
DATE_KWARGS = ["year", "month", "day", "date__gt", "gt", "date__lt", "lt"]


class CorrespondentFilterSet(FilterSet):

    class Meta:
        model = Correspondent
        fields = {
            "name": CHAR_KWARGS
        }


class TagFilterSet(FilterSet):

    class Meta:
        model = Tag
        fields = {
            "name": CHAR_KWARGS
        }


class DocumentTypeFilterSet(FilterSet):

    class Meta:
        model = DocumentType
        fields = {
            "name": CHAR_KWARGS
        }


class TagsFilter(Filter):

    def filter(self, qs, value):
        if not value:
            return qs

        try:
            tag_ids = [int(x) for x in value.split(',')]
        except ValueError:
            return qs

        for tag_id in tag_ids:
            qs = qs.filter(tags__id=tag_id)

        return qs


class InboxFilter(Filter):

    def filter(self, qs, value):
        if value == 'true':
            return qs.filter(tags__is_inbox_tag=True)
        elif value == 'false':
            return qs.exclude(tags__is_inbox_tag=True)
        else:
            return qs


class DocumentFilterSet(FilterSet):

    is_tagged = BooleanFilter(
        label="Is tagged",
        field_name="tags",
        lookup_expr="isnull",
        exclude=True
    )

    tags__id__all = TagsFilter()

    is_in_inbox = InboxFilter()

    class Meta:
        model = Document
        fields = {

            "title": CHAR_KWARGS,
            "content": CHAR_KWARGS,

            "archive_serial_number": INT_KWARGS,

            "created": DATE_KWARGS,
            "added": DATE_KWARGS,
            "modified": DATE_KWARGS,

            "correspondent__id": ID_KWARGS,
            "correspondent__name": CHAR_KWARGS,

            "tags__id": ID_KWARGS,
            "tags__name": CHAR_KWARGS,

            "document_type__id": ID_KWARGS,
            "document_type__name": CHAR_KWARGS,

        }


class LogFilterSet(FilterSet):

    class Meta:
        model = Log
        fields = {

            "level": INT_KWARGS,
            "created": DATE_KWARGS,
            "group": ID_KWARGS

        }
