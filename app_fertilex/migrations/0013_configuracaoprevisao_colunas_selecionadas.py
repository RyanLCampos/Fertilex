# Generated by Django 4.2.5 on 2023-10-26 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fertilex', '0012_configuracaoprevisao_smote'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracaoprevisao',
            name='colunas_selecionadas',
            field=models.JSONField(default=list),
        ),
    ]
