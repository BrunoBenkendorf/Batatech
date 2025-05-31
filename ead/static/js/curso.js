function trocarAba(id, event) {
            document.querySelectorAll(".conteudo-aba").forEach((el) =>
                el.classList.remove("ativo")
            );
            document.querySelectorAll(".aba").forEach((el) => el.classList.remove("ativo"));
            document.getElementById(id).classList.add("ativo");
            event.target.classList.add("ativo");
        }
    
        function registrarVisualizacao(arquivoId) {
            fetch(`/registrar_visualizacao/${arquivoId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "ok") {
                    // ✅ Marca como visualizado
                    const linkEl = document.querySelector(`[data-id='${arquivoId}']`);
                    if (linkEl) {
                        const card = linkEl.closest(".card-conteudo");
                        let span = card.querySelector(".visualizado-span");
                        if (!span) {
                            span = document.createElement("span");
                            span.classList.add("visualizado-span");
                            span.style.color = "green";
                            span.style.marginLeft = "8px";
                            span.textContent = "✔ Visualizado";
                            card.appendChild(span);
                        }
                    }
    
                    // ✅ Atualiza a barra de progresso dinamicamente
                    const progressoTexto = document.querySelector(".barra-progresso p");
                    if (progressoTexto && data.progresso !== undefined) {
                        progressoTexto.innerHTML = progressoTexto.innerHTML.replace(
                            /Progresso do curso: <strong>.*?%<\/strong>/,
                            `Progresso do curso: <strong>${data.progresso}%</strong>`
                        );
                    }
    
                } else {
                    console.error("Erro ao registrar visualização");
                }
            })
            .catch((error) => {
                console.error("Erro na requisição:", error);
            });
        }
    
        // 🟢 Ativa clique para registrar visualização
        document.querySelectorAll('.link-arquivo').forEach(link => {
            link.addEventListener('click', function () {
                const arquivoId = this.getAttribute('data-id');
                registrarVisualizacao(arquivoId);
            });
        });
        document.addEventListener('DOMContentLoaded', () => {
    const barra = document.querySelector('.barra-progresso');
    if (barra) {
        const progresso = parseInt(barra.getAttribute('data-progresso')) || 0;
        const preenchimento = barra.querySelector('.barra-progresso-preenchimento');
        preenchimento.style.width = progresso + '%';
    }
});