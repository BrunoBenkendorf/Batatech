# BataTECH - Plataforma de Cursos EAD

## Descrição do Projeto

BataTECH é uma plataforma de cursos online em desenvolvimento, projetada para facilitar o aprendizado de alunos e a gestão de cursos por professores. Este projeto é parte do curso do 3º semestre e visa proporcionar uma experiência de aprendizado interativa e acessível.

---

## Status do Projeto

**Em Desenvolvimento:**  
O projeto ainda está em fase de desenvolvimento. Funcionalidades estão sendo implementadas e testadas.

---

## Funcionalidades Planejadas

- **Cadastro de Alunos e Professores:** Permitir que novos usuários se cadastrem na plataforma.
- **Login e Logout:** Usuários poderão fazer login e logout de suas contas.
- **Gerenciamento de Cursos:** Professores poderão criar, editar e gerenciar cursos.
- **Acesso a Materiais:** Alunos poderão acessar materiais de cursos, como PDFs, vídeos e atividades.
- **Avaliações:** Professores poderão criar avaliações e os alunos poderão responder a elas.
- **Resultados:** Alunos poderão visualizar seus resultados de avaliações.
- **Configurações de Conta:** Usuários poderão alterar suas configurações de conta, como tema e notificações.

---

## Tecnologias Utilizadas

- **Django:** Framework web utilizado para o desenvolvimento do backend.
- **HTML/CSS:** Linguagens de marcação e estilo para a construção das interfaces.
- **JavaScript:** Para interatividade nas páginas.
- **Bootstrap:** Framework CSS para design responsivo.
- **Tailwind CSS:** Utilizado para estilização moderna e flexível.

---

## Estrutura do Projeto

```
/plataforma_ead
│
├── /ead                  # Aplicação principal
│   ├── /migrations       # Migrations do banco de dados
│   ├── /templates        # Templates HTML
│   ├── /static           # Arquivos estáticos (CSS, JS, imagens)
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Lógica de visualização
│   ├── urls.py           # Rotas da aplicação
│   └── ...
│
├── manage.py             # Script de gerenciamento do Django
├── settings.py           # Configurações do projeto
└── urls.py               # Rotas do projeto
```

---

## Como Executar o Projeto

1. Clone este repositório.
2. Crie e ative um ambiente virtual Python.
3. Instale as dependências com:
   ```
   pip install -r requirements.txt
   ```
4. Aplique as migrações:
   ```
   python manage.py migrate
   ```
5. Execute o servidor local:
   ```
   python manage.py runserver
   ```
6. Acesse `http://127.0.0.1:8000` no navegador para usar a plataforma.

---

## Contato

Para dúvidas, sugestões ou contribuições, entre em contato pelo email: seuemail@exemplo.com

---

*Projeto desenvolvido para fins acadêmicos - 3º semestre*
