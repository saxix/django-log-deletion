import pytest
from django.db.transaction import atomic
from django_dynamic_fixture import G

from demoproject.models import DemoModel, DemoModel2
from log_deletion.models import Deletion, registry

from log_deletion.utils import monitor_deletion, disable_log_deletion, log_deletion


def setup():
    monitor_deletion(DemoModel)
    monitor_deletion(DemoModel2)


def teardown():
    for model in list(registry):
        registry.remove(model)


@pytest.mark.django_db(transaction=True)
def test_deletion_simple():
    record = G(DemoModel)
    id = record.pk

    # monitor(DemoModel)
    with atomic():
        record.delete()
    assert Deletion.objects.filter(object_id=id)


@pytest.mark.django_db(transaction=True)
def test_deletion_multiple():
    records = G(DemoModel, n=10)
    id = records[0].pk
    # monitor(DemoModel)

    with atomic():
        DemoModel.objects.filter(id__gt=id).delete()
    assert Deletion.objects.count() == 9


@pytest.mark.django_db(transaction=True)
def test_disable_log_deletion():
    record = G(DemoModel)
    id = record.pk

    # monitor(DemoModel)
    with atomic():
        with disable_log_deletion(DemoModel):
            record.delete()
    assert not Deletion.objects.filter(object_id=id).exists()


@pytest.mark.django_db(transaction=True)
def test_deletion_rollback():
    record = G(DemoModel)
    id = record.pk

    # monitor(DemoModel)
    try:
        with atomic():
            record.delete()
            raise
    except:
        pass
    assert not Deletion.objects.filter(object_id=id).exists()
    assert DemoModel.objects.filter(id=id).exists()


@pytest.mark.django_db(transaction=True)
def test_deletion_multimodel():
    record1 = G(DemoModel)
    record2 = G(DemoModel2)
    id1 = record1.pk
    id2 = record2.pk

    with log_deletion(DemoModel, DemoModel2):
        with atomic():
            record2.delete()
            record1.delete()
    assert Deletion.objects.filter_model(DemoModel2).filter(object_id=id2).exists()
    assert Deletion.objects.filter_model(DemoModel).filter(object_id=id1).exists()
