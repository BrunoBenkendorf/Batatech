const temaEscuro = document.getElementById('temaEscuro');
const notificacoes = document.getElementById('notificacoes');
const volume = document.getElementById('volume');
const volumeValue = document.getElementById('volumeValue');
const velocidade = document.getElementById('velocidade');
const idioma = document.getElementById('idioma');
const notificacaoTipo = document.getElementById('notificacaoTipo');
const legendaAtiva = document.getElementById('legendaAtiva');

function aplicarTema(escuro) {
  document.body.style.background = escuro
    ? 'linear-gradient(#1a1a1a, #333)fixed'
    : 'linear-gradient(#fdf5ad, #fab663)fixed';
}

volume.addEventListener('input', () => {
  volumeValue.textContent = volume.value;
});

temaEscuro.addEventListener('change', () => {
  aplicarTema(temaEscuro.checked);
});

function salvarConfiguracoes() {
  const config = {
    temaEscuro: temaEscuro.checked,
    notificacoes: notificacoes.checked,
    volume: volume.value,
    velocidadeVideo: velocidade.value,
    idioma: idioma.value,
    notificacaoTipo: notificacaoTipo.value,
    legendaAtiva: legendaAtiva.checked
  };
  localStorage.setItem('bataTechConfig', JSON.stringify(config));
  alert('Configurações salvas!');
}

function carregarConfiguracoes() {
  const configSalva = localStorage.getItem('bataTechConfig');
  if (configSalva) {
    const config = JSON.parse(configSalva);
    temaEscuro.checked = config.temaEscuro;
    notificacoes.checked = config.notificacoes;
    volume.value = config.volume;
    volumeValue.textContent = config.volume;
    velocidade.value = config.velocidadeVideo;
    idioma.value = config.idioma;
    notificacaoTipo.value = config.notificacaoTipo;
    legendaAtiva.checked = config.legendaAtiva;
    aplicarTema(config.temaEscuro);
  }
}
carregarConfiguracoes();