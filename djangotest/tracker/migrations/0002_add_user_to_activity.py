# Generated manually

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(
                default=1,  # We'll need to update this for existing records
                on_delete=django.db.models.deletion.CASCADE,
                related_name='activities',
                to=settings.AUTH_USER_MODEL,
                verbose_name='User'
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={
                'ordering': ['-date'],
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities'
            },
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['date', 'name'], name='tracker_act_date_2c4af3_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['calories_burned', 'date'], name='tracker_act_calorie_1a9d23_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user', 'date'], name='tracker_act_user_id_8f1234_idx'),
        ),
    ] 