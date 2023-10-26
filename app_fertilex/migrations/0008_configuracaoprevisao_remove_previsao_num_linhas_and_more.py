# Generated by Django 4.2.5 on 2023-10-23 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_fertilex', '0007_previsao_num_linhas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoPrevisao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_linhas', models.IntegerField(default=0)),
                ('standard_scaler', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='previsao',
            name='num_linhas',
        ),
        migrations.AddField(
            model_name='previsao',
            name='configuracao',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_fertilex.configuracaoprevisao'),
        ),
    ]
