
getCatalogo().then(response => {mostrarCatalogo(response)})

async function getCatalogo()
{
    let response = await fetch('http://127.0.0.1:5000/getcatalogo')
    let data = await response.json()
   
    return data
}

async function mostrarCatalogo(dicionario)
{

    let nomeLivro;
    let autorLivro;
    let estoqueLivro; 
    getCatalogo()
   
    let catalogo = document.getElementById("catalogo");
    Object.entries(dicionario).forEach(([key, value]) => {
    
        /* pega os dados do json */
        nomeLivro = value['nome'];
        autorLivro = value['autor'];
        estoqueLivro = value['quantidade'];
        urlLivro = value['img'];

        let quadradoGrande = document.createElement("div");
        quadradoGrande.classList.add("col-sm-4");
        catalogo.appendChild(quadradoGrande);

        let painel1 = document.createElement("div");
        painel1.classList.add("painel1");
        quadradoGrande.appendChild(painel1);

        let painelNome = document.createElement("div");
        painelNome.classList.add("nomeLivro");
        painel1.appendChild(painelNome);
        painelNome.innerHTML = nomeLivro;
        
        let painelImg = document.createElement("img");
        painelImg.classList.add("capaLivro");
        painel1.appendChild(painelImg); 
        painelImg.src = urlLivro;

        let painelAutor = document.createElement("div");
        painelAutor.classList.add("autorLivro");
        painel1.appendChild(painelAutor);
        painelAutor.innerHTML = autorLivro;

        let painelEstoque = document.createElement("div");
        painelEstoque.classList.add("quantidadeLivro");
        painel1.appendChild(painelEstoque);
        painelEstoque.innerHTML = estoqueLivro;

    });
}