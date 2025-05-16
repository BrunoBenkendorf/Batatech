document.addEventListener('DOMContentLoaded', function () {
  const perfilAluno = document.getElementById('perfil-aluno');
  const perfilProfessor = document.getElementById('perfil-professor');
  const camposProfessor = document.getElementById('camposProfessor');
  const form = document.getElementById('cadastroForm');
  const erro = document.getElementById('erro');
  const telefoneInput = document.getElementById('telefone');
  const emailInput = document.getElementById('email');
  const cpfInput = document.getElementById('cpf');

  let emailValido = true;

  function atualizarCampos() {
    camposProfessor.classList.toggle('hidden', !perfilProfessor.checked);
  }

  perfilAluno.addEventListener('change', atualizarCampos);
  perfilProfessor.addEventListener('change', atualizarCampos);
  atualizarCampos();

  telefoneInput.addEventListener('input', function () {
    let valor = this.value.replace(/\D/g, '');
    if (valor.length > 11) {
      valor = valor.slice(0, 11);
    }
    if (valor.length <= 10) {
      this.value = valor.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3');
    } else {
      this.value = valor.replace(/^(\d{2})(\d{5})(\d{0,4})$/, '($1) $2-$3');
    }
  });
  cpfInput.addEventListener('input', function () {
    let valor = this.value.replace(/\D/g, '');
  
    if (valor.length > 11) valor = valor.slice(0, 11);
  
    if (valor.length > 9) {
      this.value = valor.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    } else if (valor.length > 6) {
      this.value = valor.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
    } else if (valor.length > 3) {
      this.value = valor.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    } else {
      this.value = valor;
    }
  });

  function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    let resto = 11 - (soma % 11);
    if (resto >= 10) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
    resto = 11 - (soma % 11);
    if (resto >= 10) resto = 0;
    return resto === parseInt(cpf.charAt(10));
  }

  // Verificação de e-mail duplicado
  emailInput.addEventListener('blur', function () {
    const email = this.value;
    fetch(`/verificar-email/?email=${encodeURIComponent(email)}`)
      .then(response => response.json())
      .then(data => {
        if (data.exists) {
          erro.textContent = 'Este e-mail já está cadastrado.';
          erro.classList.remove('hidden');
          emailValido = false;
        } else {
          erro.classList.add('hidden');
          emailValido = true;
        }
      })
      .catch(err => {
        console.error('Erro ao verificar e-mail:', err);
      });
  });

  form.addEventListener('submit', function (e) {
    const senha = document.getElementById('senha').value;
    const confirmaSenha = document.getElementById('confirmaSenha').value;
    const cpf = document.getElementById('cpf').value;
    const telefone = telefoneInput.value.replace(/\D/g, '');

    if (!emailValido) {
      erro.textContent = 'Este e-mail já está cadastrado.';
      erro.classList.remove('hidden');
      e.preventDefault();
      return;
    }

    if (senha.length < 6) {
      erro.textContent = 'A senha deve ter no mínimo 6 caracteres.';
      erro.classList.remove('hidden');
      e.preventDefault();
      return;
    }

    if (senha !== confirmaSenha) {
      erro.textContent = 'As senhas não coincidem.';
      erro.classList.remove('hidden');
      e.preventDefault();
      return;
    }

    if (!validarCPF(cpf)) {
      erro.textContent = 'CPF inválido.';
      erro.classList.remove('hidden');
      e.preventDefault();
      return;
    }

    if (telefone.length !== 11) {
      erro.textContent = 'O telefone deve conter exatamente 11 dígitos (DDD + número).';
      erro.classList.remove('hidden');
      e.preventDefault();
      return;
    }

    erro.classList.add('hidden');
  });
});

// Alternar visibilidade da senha
function toggleSenha(idInput, idIcone) {
  const input = document.getElementById(idInput);
  const icone = document.getElementById(idIcone);
  if (input.type === 'password') {
    input.type = 'text';
    icone.classList.replace('bi-eye-slash', 'bi-eye');
  } else {
    input.type = 'password';
    icone.classList.replace('bi-eye', 'bi-eye-slash');
  }
}
