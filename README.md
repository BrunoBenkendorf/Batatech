# 🎓 BataTECH - Plataforma de Cursos EAD

Este é o repositório do projeto **BataTECH**, uma plataforma de cursos online em desenvolvimento.

## 📘 Descrição do Projeto

**BataTECH** é uma plataforma de ensino a distância (EAD) desenvolvida para facilitar o aprendizado de alunos e a gestão de cursos por professores. Este projeto integra o curso de **Desenvolvimento de Sistemas (3º semestre)** e busca oferecer uma experiência de aprendizado **interativa**, **moderna** e **acessível**.

## 🚧 Status do Projeto

**Em desenvolvimento**  
Funcionalidades estão sendo implementadas e testadas continuamente.

## ✅ Funcionalidades Planejadas

- 📌 Cadastro de alunos e professores  
- 🔐 Login e logout de usuários  
- 🧑‍🏫 Gerenciamento de cursos pelos professores  
- 📂 Acesso a materiais (PDFs, vídeos, atividades)  
- 📝 Criação e resolução de avaliações  
- 📊 Visualização de resultados pelos alunos  
- ⚙️ Configurações de conta (tema, notificações etc.)  
- 🛠️ Painel administrativo para gerenciar usuários, cursos e conteúdos

## 🛠️ Tecnologias Utilizadas

- **Django** – Backend da aplicação  
- **HTML/CSS** – Estrutura e estilo das páginas  
- **JavaScript** – Funcionalidades interativas  
- **Bootstrap** – Layout responsivo com componentes prontos  
- **Tailwind CSS** – Estilização moderna e personalizada

## 📁 Estrutura do Projeto

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
└── urls.py               # Rotas principais do projeto
```

## ▶️ Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/BrunoBenkendorf/Batatech.git
   ```

2. **Acesse o diretório do projeto:**

   ```bash
   cd Batatech
   ```

3. **Crie e ative um ambiente virtual Python:**

   ```bash
   python -m venv venv
   ```

   - No Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - No macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Aplique as migrações:**

   ```bash
   python manage.py migrate
   ```

6. **Execute o servidor local:**

   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação:**

   Abra o navegador e vá para:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📬 Contato

Para dúvidas, sugestões ou contribuições, entre em contato:  
📧 brunobenkendorf11@gmail.com

## 📄 Licença

Projeto desenvolvido para fins acadêmicos – 3º semestre do curso de Desenvolvimento de Sistemas.
