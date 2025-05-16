from django.db import models


class Administrador(models.Model):
    id_administrador = models.AutoField(db_column='ID_Administrador', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100)
    senha = models.CharField(db_column='Senha', max_length=15)
    email = models.CharField(db_column='Email', max_length=45)

    class Meta:
        db_table = 'administrador'


class Aluno(models.Model):
    id_aluno = models.AutoField(db_column='ID_Aluno', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100)
    senha = models.CharField(db_column='Senha', max_length=17)
    telefone = models.CharField(db_column='Telefone', max_length=15, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=45)
    cpf = models.CharField(db_column='CPF', unique=True, max_length=15)

    class Meta:
        db_table = 'aluno'


class Curso(models.Model):
    id_curso = models.AutoField(db_column='ID_Curso', primary_key=True)
    nome = models.CharField(max_length=235, unique=True)
    descricao = models.TextField()
    objetivo = models.TextField()
    carga_horaria = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    imagem = models.ImageField(upload_to='imagens')

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'curso'


class Professor(models.Model):
    id_professor = models.AutoField(db_column='ID_Professor', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=100)
    senha = models.CharField(db_column='Senha', max_length=15)
    telefone = models.CharField(db_column='Telefone', max_length=15, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=45)
    cpf = models.CharField(db_column='CPF', unique=True, max_length=15)
    experiencia = models.CharField(db_column='Experiencia', max_length=45)
    formacao = models.CharField(db_column='Formacao', max_length=20)

    class Meta:
        db_table = 'professor'


class Modulo(models.Model):
    id_modulo = models.AutoField(db_column='ID_Modulo', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=45)
    curso_id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso_ID_Curso')

    class Meta:
        db_table = 'modulo'


class Aula(models.Model):
    id_aula = models.AutoField(db_column='ID_Aula', primary_key=True)
    titulo = models.CharField(db_column='Titulo', max_length=45, blank=True, null=True)
    modulo_id_modulo = models.ForeignKey(Modulo, models.DO_NOTHING, db_column='Modulo_ID_Modulo')
    professor_id_professor = models.ForeignKey(Professor, models.DO_NOTHING, db_column='Professor_ID_Professor')

    class Meta:
        db_table = 'aula'


class Arquivo(models.Model):
    id_arquivo = models.AutoField(db_column='ID_Arquivo', primary_key=True)
    tipo = models.CharField(db_column='Tipo', max_length=20)
    url_arquivo = models.CharField(db_column='URL_Arquivo', max_length=45)
    descricao = models.CharField(db_column='Descricao', max_length=45, blank=True, null=True)
    aula_id_aula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_ID_Aula')

    class Meta:
        db_table = 'arquivo'


class Exercicio(models.Model):
    id_exercicio = models.AutoField(db_column='ID_Exercicio', primary_key=True)
    enunciado = models.CharField(db_column='Enunciado', max_length=45)
    aula_id_aula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_ID_Aula')

    class Meta:
        db_table = 'exercicio'


class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(db_column='ID_Avaliacao', primary_key=True)
    titulo = models.CharField(db_column='Titulo', max_length=45)
    modulo_id_modulo = models.ForeignKey(Modulo, models.DO_NOTHING, db_column='Modulo_ID_Modulo')

    class Meta:
        db_table = 'avaliacao'


class Questao(models.Model):
    id_questao = models.AutoField(db_column='ID_Questao', primary_key=True)
    enunciado = models.CharField(db_column='Enunciado', max_length=45)
    tipo = models.CharField(db_column='Tipo', max_length=10)

    class Meta:
        db_table = 'questao'


class QuestaoHasAvaliacao(models.Model):
    questao_id_questao = models.ForeignKey(Questao, models.DO_NOTHING, db_column='questao_id_questao')
    avaliacao_id_avaliacao = models.ForeignKey(Avaliacao, models.DO_NOTHING, db_column='avaliacao_id_avaliacao')

    class Meta:
        db_table = 'questao_has_avaliacao'
        unique_together = (('questao_id_questao', 'avaliacao_id_avaliacao'),)


class Matricula(models.Model):
    id_matricula = models.AutoField(db_column='ID_Matricula', unique=True, primary_key=True)
    id_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='ID_Aluno')
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='ID_Curso')
    data_matricula = models.DateField(db_column='Data_Matricula')

    class Meta:
        db_table = 'matricula'


class Progresso(models.Model):
    id_progresso = models.AutoField(db_column='ID_Progresso', unique=True, primary_key=True)
    id_usuario = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='ID_Usuario')
    id_aula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='ID_Aula')
    status = models.CharField(db_column='Status', max_length=10)

    class Meta:
        db_table = 'progresso'


class Suporte(models.Model):
    id_contato = models.AutoField(db_column='ID_Contato', primary_key=True)
    tipo = models.CharField(db_column='Tipo', max_length=20)
    valor = models.CharField(db_column='Valor', max_length=50)
    disponibilidade = models.CharField(db_column='Disponibilidade', max_length=20)

    class Meta:
        db_table = 'suporte'


class MensagemContato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensagem_contato'