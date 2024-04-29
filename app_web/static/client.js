// getCatalogo().then(response => {console.log(response)})
getCatalogo().then(response => {mostrarCatalogo(response)})
// baixarCatalogo().then()
// removerlivro().then(data => {})
// mostrarCatalogo().then(response =>{console.log(response)})
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
    //criar novos items referentes ao dicionario e dar append na div dos catalogos
    // document.getElementById("capaLivro").src = "https://m.media-amazon.com/images/I/51i7kH+rh9L._SY445_SX342_.jpg";

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
        // painelImg.innerHTML = urlLivro;
        painelImg.src = urlLivro;

        let painelAutor = document.createElement("div");
        painelAutor.classList.add("autorLivro");
        painel1.appendChild(painelAutor);
        painelAutor.innerHTML = autorLivro;

        let painelEstoque = document.createElement("div");
        painelEstoque.classList.add("quantidadeLivro");
        painel1.appendChild(painelEstoque);
        painelEstoque.innerHTML = estoqueLivro;

        
        // console.log(value)
    });
}

{/* <div class="col-sm-4">
<div class="panel panel-primary">
  <div class="panel-heading">BLACK FRIDAY DEAL</div>
  <div class="panel-body"><img src="https://placehold.it/150x80?text=IMAGE" class="img-responsive" style="width:100%" alt="Image"></div>
  <div class="panel-footer">Buy 50 mobiles and get a gift card</div>
</div>
</div> */}

// const element = document.getElementById

function addLivro()
{

}

async function removerlivro(nome)
{
    let id = buscarLivro(await getCatalogo(), "É assim que acaba")
    let response = await fetch(`http://127.0.0.1:5000/removerlivro/${id}`, { method: 'DELETE' })
    let data = await response.json()

    console.log(data)
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

// async function baixarCatalogo()
// {
//     /*
//         Faz o fetch da requisição
//     */
//     let response = await fetch(`http://127.0.0.1:5000/download`, { method: 'GET' }) 

//     /*
//         Transforma a resposta em um binário, já que representa um arquivo
//     */
//     const fileContents = await response.blob();

//     /*
//         Tag de link no html tem um atributo 'download', que baixa o arquivo no link referido.
//         Cria um link e deixa invisivel.
//     */
//     const a = document.createElement("a");
//     a.style.display = 'none'

//     /*
//         Gera um link com o binario e indica na tag de link
//     */
//     const url = URL.createObjectURL(fileContents);
//     a.href = url;

//     /*
//         Indica o nome do arquivo que vai fazer o download
//     */ 
//     a.download = "catalogo.zip";

//     /*
//         Clica no link
//     */
//     a.click();

//     /*
//         Deleta o link temporario
//     */
//     URL.revokeObjectURL(url);

//     alert("Catálogo baixado com sucesso!"); 
// }
