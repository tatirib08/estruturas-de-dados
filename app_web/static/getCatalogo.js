
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

    // criar novos items referentes ao dicionario e dar append na div dos catalogos
    // document.getElementById("capaLivro").src = "https://m.media-amazon.com/images/I/51i7kH+rh9L._SY445_SX342_.jpg";

    /*

        <div class="container col-sm-4 rectangle p-2">  
            <p class="h5 text-center">É assim que acaba</p>
            <div class="container-fluid d-flex justify-content-center mb-3">
                <img src="https://m.media-amazon.com/images/I/9112cWOV-OL._SY385_.jpg"></img>
            </div>
            <p class="h6 text-center">Autor: <span class="h6">Colleen Hoover</span></p>
            <p class="h6 text-center">Estoque: <span class="h6">5</span></p>
        </div>

    */


    let catalogo = document.getElementById("catalogo");
    Object.entries(dicionario).forEach(([key, value]) => {
    
        /* pega os dados do json */
        nomeLivro = value['nome'];
        autorLivro = value['autor'];
        estoqueLivro = value['quantidade'];
        urlLivro = value['img'];

        let quadradoGrande = document.createElement("div");
        quadradoGrande.className += "container col-sm-3 rectangle p-2"
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


        // console.log(value)
    });
}