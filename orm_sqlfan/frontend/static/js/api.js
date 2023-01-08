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
