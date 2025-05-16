document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".btn.btn-white.btn-animated[href='#']").addEventListener("click", function (e) {
    e.preventDefault();

    const form = document.getElementById("cursoForm");
    const formData = new FormData();

    // Campos de texto
    formData.append("tituloCurso", document.getElementById("tituloCurso").value);
    formData.append("descricaoCurso", document.getElementById("descricaoCurso").value);
    formData.append("Objetivo", document.getElementById("Objetivo").value);
    formData.append("duracaoCurso", document.getElementById("duracaoCurso").value);
    formData.append("valorCurso", document.getElementById("valorCurso").value);

    // Imagem
    const imagemInput = document.getElementById("imagemCurso");
    if (imagemInput.files.length > 0) {
      formData.append("imagemCurso", imagemInput.files[0]);
    }

    fetch("/ead/salvar_curso/", {
      method: "POST",
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      alert(data);
      form.reset();
      const preview = document.getElementById("preview");
      if (preview) preview.classList.add("hidden");
    })
    .catch(error => {
      alert("Erro ao cadastrar curso.");
      console.error("Erro:", error);
    });
  });
});
