// pega a lista vazia do html
const listaElement = document.querySelector('#lista');

// conecta com o json (como uma api)
fetch('http://localhost:8000/listagem2').then((res)=> {
    return res.json();
}).then((filmes) => {
    // mapeia os filmes e renderiza cada um deles
    filmes.map((lista)=> {
        listaElement.innerHTML +=`
        <article class='containerFilme'>
            <div class='displayFilme'>
                <img src="${lista.capa}"/>
                <div class='infosFilme'>
                    <h2>${lista.nome}</h2>
                    <p><strong>Atores:</strong> ${lista.atores}</p>
                    <p><strong>Diretor:</strong> ${lista.diretor}</p>
                    <p><strong>Lançamento:</strong> ${lista.ano}</p>
                    <p><strong>Gêneros:</strong> ${lista.generos}</p>
                    <p><strong>Produtora:</strong> ${lista.produtora}</p>
                    <strong>Sinopse</strong> ${lista.sinopse}
                </div>
                <div class="buttons">
                    <button><img src="./midia/delete_btn.png" alt="Deletar"/><button>
                    <button><img src="./midia/edit_btn.png" alt="Editar"/><button>
                </div>
            </div>
        </article>
        `
    })
})