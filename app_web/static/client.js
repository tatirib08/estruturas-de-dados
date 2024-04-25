
// getCatalogo().then(response => {console.log(response)})
removerlivro().then(data => {})

async function getCatalogo()
{
    let response = await fetch('http://127.0.0.1:5000/getcatalogo')
    let data = await response.json()
   
    return data
}

function mostrarCatalogo()
{
    //limpar div dos catalogos
    
    //criar novos items referentes ao dicionario e dar append na div dos catalogos
}

{/* <div class="col-sm-4">
<div class="panel panel-primary">
  <div class="panel-heading">BLACK FRIDAY DEAL</div>
  <div class="panel-body"><img src="https://placehold.it/150x80?text=IMAGE" class="img-responsive" style="width:100%" alt="Image"></div>
  <div class="panel-footer">Buy 50 mobiles and get a gift card</div>
</div>
</div> */}


async function removerlivro(nome)
{
    let id = buscarLivro(await getCatalogo(), "É assim que acaba")
    let response = await fetch(`http://127.0.0.1:5000/removerlivro/${id}`, { method: 'DELETE' })
    let data = await response.json()

    console.log(data)
}

function buscarLivro(dicionario, nomeDoLivro)
{   
    // console.log(dicionario)
    Object.entries(dicionario).forEach(([key, value]) => {
        if(value['nome'] == nomeDoLivro)
        {
            return key
        }
        console.log(value)
    });
}
