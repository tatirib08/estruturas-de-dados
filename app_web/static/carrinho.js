
import { removerDoCarrinho, lerCarrinho, limparCarrinho } from "./crud_carrinho.js";
window.removerDoCarrinho = removerDoCarrinho


getCatalogo().then(response => {mostrarCarrinho(response)})

async function getCatalogo()
{
    let response = await fetch('http://127.0.0.1:5000/getcatalogo')
    let data = await response.json()
   
    return data
}

function mostrarCarrinho(dicionario)
{
    let nomeLivro;
    let autorLivro;
    let precoLivro;
    let urlLivro;
    let soma_valor = 0.0
    let items_carrinho = lerCarrinho()

    let count = {};
    items_carrinho.forEach(num => {
        if (count[num]) {
            count[num]++;
        } else {
            count[num] = 1;
        }
    });

    // Criando o vetor sem repetições
    let carrinho_sem_repeticao = [...new Set(items_carrinho)];

    let carrinho = document.getElementById("carrinho-items");
    carrinho.innerHTML = ""

    if(Object.keys(dicionario).length != 0)
    {
        Object.entries(dicionario).forEach(([key, value]) => {
            if(carrinho_sem_repeticao.includes(key))
            {
                /* pega os dados do json */
                nomeLivro = value['nome'];
                autorLivro = value['autor'];
                precoLivro = value['preco']
                urlLivro = value['img'];

                let quantidade = (key in count) ? count[key] : 1

                let item_carrinho = document.createElement("div");

                item_carrinho.className += "item-carrinho"
                item_carrinho.innerHTML = 
                `
                <div class="foto-item-carrinho">
                    <img src="${urlLivro}" alt="">
                </div>
                <div class="informacoes-item-carrinho">
                    <div class="titulo fonte mb-0 p-0">${nomeLivro}</div>
                    <div class="autor fonte mb-2 p-0">${autorLivro}</div>
                    <div class="quantidade fonte">Quantidade: ${quantidade}</div>
                </div>
                <div class="preco-item-carrinho fonte">
                    R$${(precoLivro * quantidade).toFixed(2)}
                </div>
                <div class="div-btn-excluir fonte ml-3">
                    <form onsubmit="removerDoCarrinho(${key})">
                        <input type="submit" class="fonte btn-sm btn-light border align-center" value="X">
                    </form>
                </div>
                `
                carrinho.appendChild(item_carrinho)

                soma_valor += parseFloat(precoLivro * quantidade)
            }
            
        });

        let total_quantidade_div = document.getElementById("total-items-resumo-carrinho")
        total_quantidade_div.innerHTML = `Total de items: ${lerCarrinho().length}`
        let total_custo_div = document.getElementById("total-valor-resumo-carrinho")
        total_custo_div.innerHTML = `Valor do carrinho: R$${soma_valor.toFixed(2)}`

        let div_frete = document.getElementById("div-frete");
        let botaoFinalizarCompra = document.getElementById("botao-finalizar-compra");
        
        let frete = localStorage.getItem("frete")
        let resultado = document.createElement("div")
        if(frete && items_carrinho.length != 0)
        {
            resultado.innerHTML = "Valor do frete: R$" + JSON.parse(frete).toFixed(2)
            let total_compra_div = document.getElementById("total-valor-compra")
            total_compra_div.innerHTML = `Valor total compra: R$${(parseFloat(soma_valor) + parseFloat(frete)).toFixed(2)}`

            botaoFinalizarCompra.addEventListener('click', () => {
                limparCarrinho();
                localStorage.removeItem('frete')
                window.location.href = "http://127.0.0.1:5000/comprafinalizada";
            })
        }
        else
        {
            botaoFinalizarCompra.disabled = true
        }
        if(items_carrinho.length == 0)
        {
            let botaoEscolherEndereco = document.getElementById("botao-escolher-endereco");
            botaoEscolherEndereco.disabled = true
        }
        if(!frete)
        {
            resultado.innerHTML = "É necessário calcular o frete!"
        }



        div_frete.appendChild(resultado)
    }
    else
    {
        let msg = document.createElement("h4");
        msg.className += "fonte"
        msg.innerHTML = "O carrinho está vazio."
        carrinho.appendChild(msg);
    }
}