const api_get = '/api/libro_view/'
//api/libro_view/?titulo__contains=sql


export async function obtenerLibros(filtro) {
    let filtrar = (filtro.toUpperCase() =='TODOS') ? '' : '?titulo__contains=' + filtro  
    let ruta_api = api_get + filtrar
    const response = await fetch( ruta_api , {
        method: 'GET'
    });

    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(Error(response.statusText));
    }
}


export async function obtenerDetalleLibro(isbn) {
    let ruta_api = api_get + isbn
    const response = await fetch( ruta_api , {
        method: 'GET'
    });

    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(Error(response.statusText));
    }
}

export async function guardarLibro(isbn, paginas, desc_corta){
    const ruta_api = api_get + isbn + '/'
    
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const cadena = JSON.stringify({
        "isbn": isbn,
        "paginas": paginas,
        "desc_corta": desc_corta
      }); 

      const requestOptions = {
        method: 'PUT',
        headers: myHeaders,
        body: cadena,
      };
    const response = await fetch(ruta_api, requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));

    return response
}