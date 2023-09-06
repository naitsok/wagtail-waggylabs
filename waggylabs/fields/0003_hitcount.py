# -*- coding: utf-8 -*-
import random, string
from django.db import migrations


def add_hit(apps, schema_editor):
    
    SitePage = apps.get_model("waggylabs.SitePage")
    HitCount = apps.get_model("hitcount.HitCount")
    Hit = apps.get_model("hitcount.Hit")
    
    letters = string.ascii_lowercase + '012345789'
    sitepage = SitePage.objects.first()
    # hit_count = HitCount.objects.get(id=sitepage.hit_count.id)
    hit_count, created = HitCount.objects.get_or_create(
            content_type=sitepage.content_type, object_pk=sitepage.pk)
    
    hit = Hit(
        ip='127.0.0.1',
        session=''.join(random.choice(letters) for i in range(40)),
        user_agent='Firefox',
        hitcount=hit_count,
    )
    hit.save()
    # hit_count.increase()
    
    
def remove_hit(apps, schema_editor):
    Hit = apps.get_model("hitcount.Hit")
    Hit.objects.first().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("waggylabs", "0002_create_sitepage"),
    ]

    operations = [
        migrations.RunPython(add_hit, remove_hit),
    ]