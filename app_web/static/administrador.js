getCatalogo().then(response => {mostrarCatalogoAdmin(response)})

async function getCatalogo()
{
    let response = await fetch('http://127.0.0.1:5000/getcatalogo')
    let data = await response.json()
   
    return data
}

async function removerlivro(nome)
{
    let id = buscarLivro(await getCatalogo(), "É assim que acaba")
    let response = await fetch(`http://127.0.0.1:5000/removerlivro/${id}`, { method: 'DELETE' })
    let data = await response.

    console.log(data)
}

async function baixarCatalogo()
{
    /*
        Faz o fetch da requisição
    */
    let response = await fetch(`http://127.0.0.1:5000/download`, { method: 'GET' }) 

    /*
        Transforma a resposta em um binário, já que representa um arquivo
    */
    const fileContents = await response.blob();

    /*
        Tag de link no html tem um atributo 'download', que baixa o arquivo no link referido.
        Cria um link e deixa invisivel.
    */
    const a = document.createElement("a");
    a.style.display = 'none'

    /*
        Gera um link com o binario e indica na tag de link
    */
    const url = URL.createObjectURL(fileContents);
    a.href = url;

    /*
        Indica o nome do arquivo que vai fazer o download
    */ 
    a.download = "catalogo.zip";

    /*
        Clica no link
    */
    a.click();

    /*
        Deleta o link temporario
    */
    URL.revokeObjectURL(url);

    alert("Catálogo baixado com sucesso!"); 
}

async function mostrarCatalogoAdmin(dicionario)
{
    let nomeLivro;
    let autorLivro;
    let estoqueLivro; 
    let precoLivro;
    let urlLivro;

    let catalogo = document.getElementById("catalogo");

    catalogo.innerHTML = ""

    if(Object.keys(dicionario).length !=0 )
    {
        Object.entries(dicionario).forEach(([key, value]) => {
        
            /* pega os dados do json */
            nomeLivro = value['nome'];
            autorLivro = value['autor'];
            precoLivro = value['preco']
            estoqueLivro = value['quantidade'];
            urlLivro = value['img'];

    
            let quadradoGrande = document.createElement("div");
            quadradoGrande.className += "fonte container col-sm-2 rectangle p-2"
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

            let painelPreco = document.createElement("p");
            painelPreco.className += "h6 text-center align-self-end";
            painelPreco.innerHTML = "Preço: R$" + precoLivro;
            quadradoGrande.appendChild(painelPreco);
    
            let painelEstoque = document.createElement("p");
            painelEstoque.className += "quantidadeLivro h6 text-center align-self-end";
            painelEstoque.innerHTML = "Estoque: " + estoqueLivro;
            quadradoGrande.appendChild(painelEstoque);


    
            let divBotoes = document.createElement("div");
            divBotoes.className += "d-flex flex-row align-content-center justify-content-around"
            quadradoGrande.appendChild(divBotoes);

            let formAdd = document.createElement("form");
            formAdd.action = `http://127.0.0.1:5000/addEstoque/${key}`
            
            let inputAdd = document.createElement("input");
            inputAdd.className += "fonte btn-sm btn-light border"
            inputAdd.value = "+"; 
            inputAdd.type = "submit";
            formAdd.appendChild(inputAdd); 
            divBotoes.appendChild(formAdd);
    
    
            let formSub = document.createElement("form");
            formSub.action = `http://127.0.0.1:5000/subEstoque/${key}`
            let inputSub = document.createElement("input");
            inputSub.className += "fonte btn-sm btn-light border"
            inputSub.value = "  -  "; 
            inputSub.type = "submit";
            formSub.appendChild(inputSub); 
            divBotoes.appendChild(formSub);

            let formDel = document.createElement("form");
            formDel.action = `http://127.0.0.1:5000/removerlivro/${key}`
            let inputDel = document.createElement("input");
            inputDel.className += "fonte btn-sm btn-light border"
            inputDel.value = "X"; 
            inputDel.type = "submit";
            formDel.appendChild(inputDel); 
            divBotoes.appendChild(formDel);
        });

    }
    else
    {
        let msg = document.createElement("h4");
        msg.className += "fonte"
        msg.innerHTML = "O livro não está no catálogo."
        catalogo.appendChild(msg);
    }

}