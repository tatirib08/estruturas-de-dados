
getCatalogo().then(response => {mostrarCatalogo(response)})

inputBusca = botaoBusca = document.getElementById("fsearch")
botaoBusca = document.getElementById("fsearchbtn")

botaoBusca.addEventListener('click', () => {
    catalogo = getCatalogo().then(
        catalogo =>
        {
            if(verificarBusca())
            {
                let escolhido = {}
                        
                Object.entries(catalogo).forEach(([key, value]) => {
                    if(value['nome'] == inputBusca.value)
                    {
                        escolhido[key] = value;
                    }
                })
                mostrarCatalogo(escolhido).then(data => {});
        
            }
            else
            {
                mostrarCatalogo(catalogo).then(data => {});
            }
        }
    )
})

async function getCatalogo()
{
    let response = await fetch('http://127.0.0.1:5000/getcatalogo')
    let data = await response.json()
   
    return data
}

function verificarBusca()
{
    let fsearch = document.getElementById("fsearch");
    let regex = /^ *$/;
    return !regex.test(fsearch.value)
}

async function mostrarCatalogo(dicionario)
{

    let nomeLivro;
    let autorLivro;
    let estoqueLivro; 

    let catalogo = document.getElementById("catalogo");

    catalogo.innerHTML = ""

    Object.entries(dicionario).forEach(([key, value]) => {
    
        /* pega os dados do json */
        nomeLivro = value['nome'];
        autorLivro = value['autor'];
        estoqueLivro = value['quantidade'];
        urlLivro = value['img'];


        let quadradoGrande = document.createElement("div");
        quadradoGrande.className += " fonte container col-sm-3 rectangle p-2"
        catalogo.appendChild(quadradoGrande);

        let painelNome = document.createElement("p");
        painelNome.className += "h5 text-center";
        quadradoGrande.appendChild(painelNome);
        painelNome.innerHTML = nomeLivro;
        
        let divImg = document.createElement("div");
        divImg.className += "container-fluid d-flex justify-content-center mb-3"
        quadradoGrande.appendChild(divImg);

        let painelImg = document.createElement("img");
        painelImg.className += "capaLivro img-fluid";
        painelImg.src = urlLivro;
        divImg.appendChild(painelImg); 

        let painelAutor = document.createElement("p");
        painelAutor.className += "autorLivro h6 text-center align-self-end";
        painelAutor.innerHTML = "Autor: " + autorLivro;
        quadradoGrande.appendChild(painelAutor);

        let painelEstoque = document.createElement("p");
        painelEstoque.className += "quantidadeLivro h6 text-center align-self-end";
        painelEstoque.innerHTML = "Estoque: " + estoqueLivro;
        quadradoGrande.appendChild(painelEstoque);

        let formAdd = document.createElement("form");
        formAdd.action = `http://127.0.0.1:5000/addEstoque/${key}`
        
        let inputAdd = document.createElement("input");
        inputAdd.className += "fonte btn-sm mr-2"
        inputAdd.value = "+"; 
        inputAdd.type = "submit";
        formAdd.appendChild(inputAdd); 
        quadradoGrande.appendChild(formAdd);


        let formSub = document.createElement("form");
        formSub.action = `http://127.0.0.1:5000/subEstoque/${key}`
        let inputSub = document.createElement("input");
        inputSub.className += "fonte btn-sm mr-2"
        inputSub.value = "-"; 
        inputSub.type = "submit";
        formSub.appendChild(inputSub); 
        quadradoGrande.appendChild(formSub);

    });
}