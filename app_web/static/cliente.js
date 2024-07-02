import { adicionarAoCarrinho, lerCarrinho, verificarSeProdutoEstaNoCarrinho } from "./crud_carrinho.js"

getCatalogo().then(response => {mostrarCatalogo(response)})

let inputBusca = document.getElementById("fsearch")
let botaoBusca = document.getElementById("fsearchbtn")

let botaoDefinirIntervalo = document.getElementById("botao-definir-intervalo") 
let divBuscaIntervalo = document.getElementById("quadradoGrande")

let botaoFecharIntervalo = document.getElementById("busca-intervalo-botao-fechar")

let formIntervalo = document.getElementById("myForm");

let quantidadeCarrinho = document.getElementById("quantidade-items-carrinho")
quantidadeCarrinho.innerHTML = lerCarrinho().length

botaoBusca.addEventListener('click', () => {
    let catalogo = getCatalogo().then(
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

    if(!validarBuscaIntervalo())
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

            let divBotoes = document.createElement("div");
            divBotoes.className += "align-content-center justify-content-center text-center row"
            quadradoGrande.appendChild(divBotoes);
            
            if(!verificarSeProdutoEstaNoCarrinho(key))
            {
                let inputAdd = document.createElement("input");
                inputAdd.className += "fonte btn-sm btn-light border"
                inputAdd.value = "Adicionar ao carrinho"; 
                inputAdd.type = "submit";
                let formAdd = document.createElement("form");
                formAdd.action = ''
                formAdd.appendChild(inputAdd); 
                inputAdd.addEventListener("click", () => {adicionarAoCarrinho(key)})
                divBotoes.appendChild(formAdd);
            }
            else
            {
                let textoJaAdicionado = document.createElement("p");
                textoJaAdicionado.className += "fonte btn-sm"
                textoJaAdicionado.innerHTML = "Já adicionado ao carrinho"
                divBotoes.appendChild(textoJaAdicionado);
                let inputAdd = document.createElement("input");
                inputAdd.className += "fonte btn-sm btn-light border"
                inputAdd.value = "Adicionar outro"; 
                inputAdd.type = "submit";
                let formAdd = document.createElement("form");
                formAdd.action = ''
                formAdd.appendChild(inputAdd); 
                inputAdd.addEventListener("click", () => {adicionarAoCarrinho(key)})
                divBotoes.appendChild(formAdd);
               
            }
        
    
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
    if(parseInt(fmax) < parseInt(fmin))
    {
      alert("O valor máximo deve ser maior que o valor mínimo");
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

function buscarLivro(dicionario, nomeDoLivro)
{   
    Object.entries(dicionario).forEach(([key, value]) => {
        if(value['nome'] == nomeDoLivro)
        {
            return key
        }
        console.log(value)
    });
}