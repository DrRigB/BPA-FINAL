from django.db import migrations

def forward_func(apps, schema_editor):
    Activity = apps.get_model('tracker', 'Activity')
    User = apps.get_model('accounts', 'CustomUser')
    
    # Get the first user or create one if none exists
    default_user = User.objects.first()
    
    if default_user:
        # Update all activities that don't have a user
        Activity.objects.filter(user__isnull=True).update(user=default_user)

def reverse_func(apps, schema_editor):
    Activity = apps.get_model('tracker', 'Activity')
    Activity.objects.all().update(user=None)

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_rename_tracker_act_date_2c4af3_idx_tracker_act_date_208f4a_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func),
    ] 