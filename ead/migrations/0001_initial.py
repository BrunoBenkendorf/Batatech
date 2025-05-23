

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_administrador', models.AutoField(db_column='ID_Administrador', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=100)),
                ('senha', models.CharField(db_column='Senha', max_length=15)),
                ('email', models.CharField(db_column='Email', max_length=45)),
            ],
            options={
                'db_table': 'administrador',
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id_aluno', models.AutoField(db_column='ID_Aluno', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=100)),
                ('senha', models.CharField(db_column='Senha', max_length=17)),
                ('telefone', models.CharField(blank=True, db_column='Telefone', max_length=15, null=True)),
                ('email', models.CharField(db_column='Email', max_length=45)),
                ('cpf', models.CharField(db_column='CPF', max_length=15, unique=True)),
            ],
            options={
                'db_table': 'aluno',
            },
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id_aula', models.AutoField(db_column='ID_Aula', primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, db_column='Titulo', max_length=45, null=True)),
            ],
            options={
                'db_table': 'aula',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id_curso', models.AutoField(db_column='ID_Curso', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=235, unique=True)),
                ('descricao', models.TextField()),
                ('objetivo', models.TextField()),
                ('carga_horaria', models.IntegerField()),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('imagem', models.ImageField(upload_to='imagens')),
            ],
            options={
                'db_table': 'curso',
            },
        ),
        migrations.CreateModel(
            name='MensagemContato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('assunto', models.CharField(max_length=200)),
                ('mensagem', models.TextField()),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'mensagem_contato',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id_professor', models.AutoField(db_column='ID_Professor', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=100)),
                ('senha', models.CharField(db_column='Senha', max_length=15)),
                ('telefone', models.CharField(blank=True, db_column='Telefone', max_length=15, null=True)),
                ('email', models.CharField(db_column='Email', max_length=45)),
                ('cpf', models.CharField(db_column='CPF', max_length=15, unique=True)),
                ('experiencia', models.CharField(db_column='Experiencia', max_length=45)),
                ('formacao', models.CharField(db_column='Formacao', max_length=20)),
            ],
            options={
                'db_table': 'professor',
            },
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id_questao', models.AutoField(db_column='ID_Questao', primary_key=True, serialize=False)),
                ('enunciado', models.CharField(db_column='Enunciado', max_length=255)),
                ('tipo', models.CharField(db_column='Tipo', max_length=10)),
                ('alternativa_a', models.CharField(max_length=255)),
                ('alternativa_b', models.CharField(max_length=255)),
                ('alternativa_c', models.CharField(max_length=255)),
                ('alternativa_d', models.CharField(max_length=255)),
                ('resposta_correta', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
            ],
            options={
                'db_table': 'questao',
            },
        ),
        migrations.CreateModel(
            name='Suporte',
            fields=[
                ('id_contato', models.AutoField(db_column='ID_Contato', primary_key=True, serialize=False)),
                ('tipo', models.CharField(db_column='Tipo', max_length=20)),
                ('valor', models.CharField(db_column='Valor', max_length=50)),
                ('disponibilidade', models.CharField(db_column='Disponibilidade', max_length=20)),
            ],
            options={
                'db_table': 'suporte',
            },
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('descricao', models.CharField(default='Descrição não informada', max_length=255)),
                ('url_arquivo', models.FileField(upload_to='arquivos/')),
                ('aula_id_aula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ead.aula')),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id_exercicio', models.AutoField(db_column='ID_Exercicio', primary_key=True, serialize=False)),
                ('enunciado', models.CharField(db_column='Enunciado', max_length=45)),
                ('aula_id_aula', models.ForeignKey(db_column='Aula_ID_Aula', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.aula')),
            ],
            options={
                'db_table': 'exercicio',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id_matricula', models.AutoField(db_column='ID_Matricula', primary_key=True, serialize=False, unique=True)),
                ('data_matricula', models.DateField(db_column='Data_Matricula')),
                ('id_aluno', models.ForeignKey(db_column='ID_Aluno', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.aluno')),
                ('id_curso', models.ForeignKey(db_column='ID_Curso', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.curso')),
            ],
            options={
                'db_table': 'matricula',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id_modulo', models.AutoField(db_column='ID_Modulo', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=45)),
                ('curso_id_curso', models.ForeignKey(db_column='Curso_ID_Curso', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.curso')),
            ],
            options={
                'db_table': 'modulo',
            },
        ),
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id_avaliacao', models.AutoField(db_column='ID_Avaliacao', primary_key=True, serialize=False)),
                ('titulo', models.CharField(db_column='Titulo', max_length=45)),
                ('modulo_id_modulo', models.ForeignKey(db_column='Modulo_ID_Modulo', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.modulo')),
            ],
            options={
                'db_table': 'avaliacao',
            },
        ),
        migrations.AddField(
            model_name='aula',
            name='modulo_id_modulo',
            field=models.ForeignKey(db_column='Modulo_ID_Modulo', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.modulo'),
        ),
        migrations.AddField(
            model_name='aula',
            name='professor_id_professor',
            field=models.ForeignKey(db_column='Professor_ID_Professor', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.professor'),
        ),
        migrations.CreateModel(
            name='Progresso',
            fields=[
                ('id_progresso', models.AutoField(db_column='ID_Progresso', primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(db_column='Status', max_length=10)),
                ('id_aula', models.ForeignKey(db_column='ID_Aula', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.aula')),
                ('id_usuario', models.ForeignKey(db_column='ID_Usuario', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.aluno')),
            ],
            options={
                'db_table': 'progresso',
            },
        ),
        migrations.CreateModel(
            name='QuestaoHasAvaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao_id_avaliacao', models.ForeignKey(db_column='avaliacao_id_avaliacao', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.avaliacao')),
                ('questao_id_questao', models.ForeignKey(db_column='questao_id_questao', on_delete=django.db.models.deletion.DO_NOTHING, to='ead.questao')),
            ],
            options={
                'db_table': 'questao_has_avaliacao',
                'unique_together': {('questao_id_questao', 'avaliacao_id_avaliacao')},
            },
        ),
    ]
