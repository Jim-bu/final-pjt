# Generated by Django 4.2.16 on 2024-11-22 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositBaseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.CharField(max_length=6)),
                ('fin_co_no', models.CharField(max_length=20)),
                ('fin_prdt_cd', models.CharField(max_length=20)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=8)),
                ('dcls_end_day', models.CharField(blank=True, max_length=8, null=True)),
                ('fin_co_subm_day', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='SavingBaseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dcls_month', models.CharField(max_length=6)),
                ('fin_co_no', models.CharField(max_length=20)),
                ('fin_prdt_cd', models.CharField(max_length=20)),
                ('kor_co_nm', models.CharField(max_length=100)),
                ('fin_prdt_nm', models.CharField(max_length=100)),
                ('join_way', models.TextField()),
                ('mtrt_int', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('etc_note', models.TextField(blank=True, null=True)),
                ('max_limit', models.BigIntegerField(blank=True, null=True)),
                ('dcls_strt_day', models.CharField(max_length=8)),
                ('dcls_end_day', models.CharField(blank=True, max_length=8, null=True)),
                ('fin_co_subm_day', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='SavingOptionList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_trm', models.CharField(max_length=10)),
                ('intr_rate', models.FloatField(blank=True, null=True)),
                ('intr_rate2', models.FloatField(blank=True, null=True)),
                ('intr_rate_type', models.CharField(blank=True, max_length=10, null=True)),
                ('intr_rate_type_nm', models.CharField(blank=True, max_length=20, null=True)),
                ('dcls_month', models.CharField(max_length=6)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_options', to='bankings.savingbaselist')),
            ],
        ),
        migrations.CreateModel(
            name='DepositOptionList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_trm', models.CharField(max_length=10)),
                ('intr_rate', models.FloatField(blank=True, null=True)),
                ('intr_rate2', models.FloatField(blank=True, null=True)),
                ('intr_rate_type', models.CharField(blank=True, max_length=10, null=True)),
                ('intr_rate_type_nm', models.CharField(blank=True, max_length=20, null=True)),
                ('dcls_month', models.CharField(max_length=6)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_options', to='bankings.depositbaselist')),
            ],
        ),
    ]
