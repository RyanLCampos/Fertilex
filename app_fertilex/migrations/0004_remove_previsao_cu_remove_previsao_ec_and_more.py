# Generated by Django 4.2.5 on 2023-09-15 17:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_fertilex', '0003_resultado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previsao',
            name='Cu',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='EC',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='Fe',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='K',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='Mn',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='N',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='OC',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='P',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='S',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='Zn',
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='pH',
        ),
        migrations.AddField(
            model_name='previsao',
            name='dados_tabela',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='previsao',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='previsao',
            name='resultados',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='previsao',
            name='titulo',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.DeleteModel(
            name='Resultado',
        ),
    ]
