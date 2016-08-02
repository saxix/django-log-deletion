import pytest
from django.core.urlresolvers import reverse
from django_dynamic_fixture import G
from rest_framework.test import APIRequestFactory

from demoproject.models import DemoModel, DemoModel2
from log_deletion.models import Deletion, registry

from log_deletion.utils import monitor_deletion

factory = APIRequestFactory()


def setup():
    monitor_deletion(DemoModel)
    monitor_deletion(DemoModel2)


def teardown():
    for model in list(registry):
        registry.remove(model)


@pytest.fixture()
def deletion():
    return G(Deletion)


@pytest.mark.django_db
def test_api(client, deletion):
    url = reverse('deletions')
    res = client.get(url)
    assert res.json
