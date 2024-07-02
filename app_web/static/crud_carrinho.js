export function adicionarAoCarrinho(key)
{
    let carrinhoAtual = lerCarrinho()

    carrinhoAtual.push(key)

    localStorage.setItem('carrinho', JSON.stringify(carrinhoAtual))
}

export function removerDoCarrinho(key) {
    let carrinhoAtual = lerCarrinho();
    
    carrinhoAtual = carrinhoAtual.filter(item => item != key);
    
    localStorage.setItem('carrinho', JSON.stringify(carrinhoAtual));
}

export function lerCarrinho() {
    const carrinho = localStorage.getItem('carrinho');
    return carrinho ? JSON.parse(carrinho) : [];
}

export function limparCarrinho()
{
    localStorage.removeItem('carrinho')
}

export function verificarSeProdutoEstaNoCarrinho(key)
{
    let carrinho = lerCarrinho()

    return carrinho.includes(key)
}