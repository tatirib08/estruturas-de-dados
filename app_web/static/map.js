let btn = document.getElementById('botao-calcular-frete')

var map = L.map('map').setView([-12.94531097712202, -38.39225762988138], 16);

// marcadores 
var markerJMT = L.marker([-12.94531097712202, -38.39225762988138]).addTo(map); //1
var markerJardimBotanico = L.marker([-12.94784371419937, -38.39214893480724]).addTo(map); //2
var markerVillaIpes = L.marker([-12.950116414482098, -38.39250466411566]).addTo(map); //3
var markerVillaPalmeiras = L.marker([-12.949906039271077, -38.39215598629933]).addTo(map); //4
var markerArtResidence = L.marker([-12.949521982578934, -38.390013533999564]).addTo(map); //5 
var markerADELBA = L.marker([-12.942147663776431, -38.39392460777726]).addTo(map); //6
var markerShopParalela = L.marker([-12.9366414999585, -38.394633602340164]).addTo(map); //7 
var markerFTC = L.marker([-12.933893247744633, -38.392235968839536]).addTo(map); //8
var markerHiperIdeal = L.marker([-12.93753670636973, -38.38504546465638]).addTo(map); //9 
var markerSenai = L.marker([-12.938306329159209, -38.387108878274994]).addTo(map); //10
var markerSESI = L.marker([-12.940165609625732, -38.38657714421048]).addTo(map); //11
var markerCondCostaVerde = L.marker([-12.945719714625996, -38.38513549153101]).addTo(map); //12
var markerConcept = L.marker([-12.945480362375427, -38.38413515390469]).addTo(map); //13
var markerVeredas = L.marker([-12.950983116809434, -38.38950072777228]).addTo(map);//14
var markerCostaVerde = L.marker([-12.95261058295917, -38.38580509556764]).addTo(map); //15
var markerSESC = L.marker([-12.954748421741924, -38.387534335281124]).addTo(map); //16
var markerVilarejo = L.marker([-12.95691384110901, -38.39155066102774]).addTo(map); //17
var markerJaguaResidence = L.marker([-12.957796676884396, -38.39283508807169]).addTo(map); //18 
var markerArmazemPaulistano = L.marker([-12.957057964379649, -38.39291578761762]).addTo(map); //19 
var markerValeJaguaribe = L.marker([-12.95413038452778, -38.392621030521425]).addTo(map); //20 
var markerBotecoPipeline = L.marker([-12.956471133930867, -38.39316723884929]).addTo(map); //21
var markerJaguaItacenter = L.marker([-12.957106744543566, -38.393320775180904]).addTo(map); //22 
var markerPremiereJagua = L.marker([-12.95792746682822, -38.3935113418869]).addTo(map); //23 
var markerResidencialPatamares = L.marker([-12.953898041052389, -38.39587276289372]).addTo(map); //24
var markerResidVillaGiadirno = L.marker([-12.95280635630802, -38.395431726588335]).addTo(map); //25
var markerHortoPatamares = L.marker([-12.952093739846195, -38.39540208247184]).addTo(map); //26 

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    // attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function validarEndEscolhido()
{
    event.preventDefault();
    var input = document.getElementById("options").value;

    alert(input);
    if(input == "1")
    {
        alert("É necessário escolher um endereço");
    }
    else
    {
        fetch('http://127.0.0.1:5000/getcatalogo',{
            method: 'POST',
            body: JSON.stringify({
                "options": input
            })
        })
        .then(response => {
            // return response.json(); // Se a resposta for JSON
        })
        .then(data => {
            alert(`FRETE -> ${data}`)
            
        })
    }

    return false
}

btn.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent default form submission

    const selectedRadio = document.querySelector('input[name="options"]:checked');

    if(!selectedRadio)
    {
        alert("É necessário selecionar um endereço");
        return
    }

    try {
        let bodyData = JSON.stringify({ "options": selectedRadio.value })
        console.log("sending " + bodyData)
        const response = await fetch("http://127.0.0.1:5000/mapa", {
            method: "POST",
            body: bodyData,
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status}`);
        }

        const responseData = await response.json();
        console.log(responseData)
        localStorage.setItem('frete', JSON.stringify(responseData['frete']))
        window.location.href = "http://127.0.0.1:5000/carrinho";

    } catch (error) {
        console.error("Error:", error);
        // Handle errors appropriately (e.g., display error message)
    }
});
