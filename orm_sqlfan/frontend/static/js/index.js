import {
    obtenerLibros,
    obtenerDetalleLibro,
} from './api.js'


const btnFiltros = document.getElementById('filtros');
console.log(btnFiltros)
var clickHandler = function (index) {
    alert("Vas a filtrar por " + index);
}

function mostrarDetalleLibros(datos){
    console.log(datos)
    const input_isbn = document.getElementById('inputIsbn')
    const input_titulo = document.getElementById('inputTitulo')
    const input_paginas = document.getElementById('inputPaginas')
    const input_descripcion = document.getElementById('textDescripcion')

    input_isbn.value = datos['isbn']
    input_titulo.value = datos['titulo']
    input_paginas.value = datos['paginas']
    input_descripcion.value = datos['desc_corta']
    
}

function mostrarLibros(datos){
    const tabla = document.getElementById('listado-libros')
    tabla.innerHTML=""
    for(let i=0; i<datos.resultado.length; i++){
        console.log(datos.resultado[i])
        const libro = datos.resultado[i]

        const fila = document.createElement('tr')
        const dIsbn = document.createElement('td')
        const dTitulo = document.createElement('td')
        const dImagen = document.createElement('td')

        const ImagenLibro = document.createElement('img')
        ImagenLibro.setAttribute('src', libro['imagen'])
        ImagenLibro.setAttribute('class', libro['img-thumbnail'])


        dImagen.appendChild(ImagenLibro)

        const textIsbn = document.createTextNode(libro['isbn'])



        dIsbn.appendChild(textIsbn)
        dIsbn.addEventListener('click', function(event){
            const lib = obtenerDetalleLibro(event.target.innerHTML).then((libro )=>{ 
                mostrarDetalleLibros(libro)})
        })

        dTitulo.appendChild(document.createTextNode(libro['titulo']))

        fila.appendChild(dIsbn)
        fila.appendChild(dTitulo)
        fila.appendChild(dImagen)
        tabla.appendChild(fila)
    }
}

btnFiltros.addEventListener('click', function(event){
    const lib = obtenerLibros(event.target.innerHTML).then((libros )=>{ 
        mostrarLibros(libros)})
})
