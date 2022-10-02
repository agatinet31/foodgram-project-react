import pytest

from .serializers import TagListField, TagSerializer
from .utils import check_with_validate_data


class TestTagsAPI:
    url_tags = '/api/tags/'

    @pytest.mark.django_db(transaction=True)
    def test_list_tags(self, client, tag1, tag2, tag3):
        check_with_validate_data(
            client,
            'get',
            self.url_tags,
            serializer=TagListField
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_tag(self, client, tag1):
        url = f'{self.url_tags}{tag1.pk}/'
        check_with_validate_data(
            client,
            'get',
            url,
            serializer=TagSerializer
        )
