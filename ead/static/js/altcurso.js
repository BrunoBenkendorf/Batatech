document.getElementById("tipo").addEventListener("change", function () {
      const tipo = this.value;
      const cursoId = document.querySelector('input[name="curso_id"]').value;

      if (tipo === "prova") {
        window.location.href = `/ead/criar_avaliacao/?curso_id=${cursoId}`;
      } else if (tipo === "forum") {
        window.location.href = `/ead/criar_forum/?curso_id=${cursoId}`;
      }
    });