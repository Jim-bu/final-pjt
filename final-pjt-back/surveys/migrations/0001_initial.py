# Generated by Django 4.2.16 on 2024-11-25 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(max_length=20)),
                ('income_source', models.CharField(max_length=20)),
                ('asset_size', models.CharField(max_length=20)),
                ('financial_purpose', models.CharField(max_length=20)),
                ('important_factor', models.CharField(max_length=20)),
                ('expected_return', models.CharField(max_length=20)),
                ('investment_period', models.CharField(max_length=20)),
                ('financial_products', models.CharField(max_length=100)),
                ('preferred_bank', models.CharField(max_length=20)),
                ('banking_channel', models.CharField(max_length=20)),
                ('recent_investment', models.BooleanField()),
                ('risk_tolerance', models.CharField(max_length=20)),
                ('preferred_product', models.CharField(max_length=20)),
                ('preferred_method', models.CharField(max_length=20)),
                ('monthly_investment', models.CharField(max_length=20)),
                ('preferred_benefit', models.CharField(max_length=20)),
                ('service_priority', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
