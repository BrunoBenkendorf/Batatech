const radios = document.querySelectorAll('input[name="pagamento"]');
const detalhes = document.querySelectorAll('.detalhes');

radios.forEach(radio => {
  radio.addEventListener('change', () => {
    detalhes.forEach(div => div.style.display = 'none');
    const selecionado = document.getElementById(radio.value);
    if (selecionado) selecionado.style.display = 'block';
  });
});
function formatarCartao() {
  const input = document.getElementById("numero-cartao");
  const bandeira = document.getElementById("bandeira-cartao");

  let valor = input.value.replace(/\D/g, '');
  input.value = valor.replace(/(\d{4})(?=\d)/g, '$1 ');

  if (valor.startsWith('4')) {
    bandeira.src = 'https://img.icons8.com/color/48/visa.png';
    bandeira.style.display = 'inline';
  } else if (/^5[1-5]/.test(valor)) {
    bandeira.src = 'https://img.icons8.com/color/48/mastercard-logo.png';
    bandeira.style.display = 'inline';
  } else {
    bandeira.style.display = 'none';
  }
}

function confirmarPagamento() {
  const mensagem = document.getElementById("mensagem-status");
  const botao = document.getElementById("btn-confirmar");

  // Mostrar "Processando..."
  mensagem.style.display = "block";
  mensagem.style.color = "#555";
  mensagem.textContent = "🔄 Processando pagamento...";

  // Desativar botão temporariamente
  botao.disabled = true;
  botao.style.opacity = 0.6;
  botao.style.cursor = "not-allowed";

  setTimeout(() => {
    // Mostrar mensagem final
    mensagem.textContent = "✅ Pagamento realizado com sucesso!";
    mensagem.style.color = "green";

    // Reabilita o botão se quiser usar novamente
    botao.disabled = false;
    botao.style.opacity = 1;
    botao.style.cursor = "pointer";
  }, 2000); // 2 segundos de espera
}
