console.log(getcatalogo())

function getcatalogo()
{
    let catalogo;

    fetch('http://127.0.0.1:5000/getcatalogo')
    .then(data => {
        return data.json()
    })
    .then(post => {
        catalogo = post
    })

    return catalogo;
}

{/* <div class="col-sm-4">
<div class="panel panel-primary">
  <div class="panel-heading">BLACK FRIDAY DEAL</div>
  <div class="panel-body"><img src="https://placehold.it/150x80?text=IMAGE" class="img-responsive" style="width:100%" alt="Image"></div>
  <div class="panel-footer">Buy 50 mobiles and get a gift card</div>
</div>
</div> */}


function removerlivro(nome)
{
    // chamar buscar
    fetch(`http://127.0.0.1:5000/removerlivro/${49}`,{
    method: 'DELETE'
    })
    .then(data => {
    return data.json();
    })
    .then(post => {
    console.log(post);
    });

}

function buscarLivro(nome)
{
    getcatalogo()
    return id
}
