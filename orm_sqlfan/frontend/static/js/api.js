export async function obtenerLibros() {
    const response = await fetch(`/api/libro_view/`, {
        method: 'GET'
    });

    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(Error(response.statusText));
    }
}
