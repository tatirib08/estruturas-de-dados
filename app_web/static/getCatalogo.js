
getCatalogo().then(response => {mostrarCatalogo(response)})

inputBusca = botaoBusca = document.getElementById("fsearch")
botaoBusca = document.getElementById("fsearchbtn")

botaoDefinirIntervalo = document.getElementById("botao-definir-intervalo") 
divBuscaIntervalo = document.getElementById("quadradoGrande")

botaoFecharIntervalo = document.getElementById("busca-intervalo-botao-fechar")

formIntervalo = document.getElementById("myForm");

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

botaoDefinirIntervalo.addEventListener('click', mostrarBuscaIntervalo)

botaoFecharIntervalo.addEventListener('click', esconderBuscaIntervalo)

formIntervalo.addEventListener('submit', function(event){

    if(validarBuscaIntervalo() == false)
    {
        return false;
    }

    event.preventDefault(); 
    const formData = new FormData(this);

    fetch('http://127.0.0.1:5000/buscaIntervalo', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        return response.json(); // Se a resposta for JSON
    })
    .then(data => {
        console.log(data)
        mostrarCatalogo(data).then(data => {esconderBuscaIntervalo()})
    })
})

function mostrarBuscaIntervalo(){
    divBuscaIntervalo.style.visibility = "visible";
}

function esconderBuscaIntervalo()
{
    divBuscaIntervalo.style.visibility = "hidden";
}

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
            inputAdd.className += "fonte btn-sm "
            inputAdd.value = "+"; 
            inputAdd.type = "submit";
            formAdd.appendChild(inputAdd); 
            divBotoes.appendChild(formAdd);
    
    
            let formSub = document.createElement("form");
            formSub.action = `http://127.0.0.1:5000/subEstoque/${key}`
            let inputSub = document.createElement("input");
            inputSub.className += "fonte btn-sm  "
            inputSub.value = "  -  "; 
            inputSub.type = "submit";
            formSub.appendChild(inputSub); 
            divBotoes.appendChild(formSub);

            let formDel = document.createElement("form");
            formDel.action = `http://127.0.0.1:5000/removerlivro/${key}`
            let inputDel = document.createElement("input");
            inputDel.className += "fonte btn-sm "
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

function validarBuscaIntervalo()
{

  var input = document.getElementById("options").value;

  let fprimeiraletra = document.getElementById("fprimeiraletra").value;

  let fultimaletra = document.getElementById("fultimaletra").value;

  let fmin = document.getElementById("fmin").value;

  let fmax = document.getElementById("fmax").value;

  if(input == "1"){ //por nome
      if (!fprimeiraletra || fprimeiraletra.value=="")
      {
          alert("Informe a primeira letra")
          return false;
      }
      if (!fultimaletra || fultimaletra.value=="")
      {
          alert("Informe a ultima letra")
          return false;
      }

      if(fultimaletra < fprimeiraletra)
      {
          alert("A última letra deve ser maior que a primeira");
          return false;
      }
  }
  if(input == "2"){ //por preço
      if (!fmax || fmax.value=="")
      {
          alert("Informe o valor maximo")
          return false;
      }
      if (!fmin || fmin.value=="")
      {
          alert("Informe o valor minimo")
          return false;
      }
  }

  return true;    
}


function verificaEscolhaIntervalo()
{
  var input = document.getElementById("options").value;

  if(input == "1"){ //por nome
      document.getElementById("fprimeiraletra").disabled = false;
      document.getElementById("fultimaletra").disabled = false;
      document.getElementById("fmin").disabled = true;
      document.getElementById("fmax").disabled = true;
      
  }
  if(input == "2"){ //por preço
      document.getElementById("fmin").disabled = false;
      document.getElementById("fmax").disabled = false;
      document.getElementById("fprimeiraletra").disabled = true;
      document.getElementById("fultimaletra").disabled = true;
  
  }
}