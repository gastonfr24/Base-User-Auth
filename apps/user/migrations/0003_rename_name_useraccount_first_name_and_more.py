# Generated by Django 4.2.5 on 2023-10-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_useraccount_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="useraccount",
            old_name="name",
            new_name="first_name",
        ),
        migrations.RemoveField(
            model_name="useraccount",
            name="date_joined",
        ),
        migrations.AddField(
            model_name="useraccount",
            name="last_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="useraccount",
            name="email",
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="useraccount",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="useraccount",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
