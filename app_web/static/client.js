
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
