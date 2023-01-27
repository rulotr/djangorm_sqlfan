function varAlpine(){
    return{
        url: "http://127.0.0.1:8000/api/libro_view/",
        caja_filtro: "",
        estaCargando: true,
        detalles: {isbn: "", titulo: "",paginas:0},
        libros: [],
        mostrarDetalle: function(libro){
           this.detalles.isbn = libro.isbn
           this.detalles.titulo = libro.titulo 
           this.detalles.paginas = libro.paginas  
           this.validarDatos()  
        },
        buscar(){
            let filtrado = (this.caja_filtro=="") ? '' : '?titulo__contains=' +  this.caja_filtro
            this.apiListar(filtrado)
        },
        apiListar:function(filtrado){
            fetch(this.url + filtrado).
            then(response=> response.json()).
            then((list_libros)=>{
                this.libros = list_libros.resultado;   
                this.estaCargando=false
                this.validarDatos()
            }).
            catch(console.log)
        },
        modificarLibro:function(){
            if(this.validarDatos()){
            var datos = {method:"PUT", body: JSON.stringify(this.detalles),headers: {
            'Content-Type': 'application/json'}
             }
            fetch(this.url  + this.detalles.isbn + '/', datos)
            .then(response => {
              if(response.ok) {
                alert('Libro guardado!')
                this.buscar()
            }
              else{alert('No se pudo guardar el libro') }
            }).
            catch( error=>
                alert('No se pudo guardar el libro')
            )
        }
        },
        validarDatos:function(){
                const isbn_valido = this.detalles.isbn.length>=10
                this.$refs.botonGuardar.disabled=!isbn_valido;
                return isbn_valido
        }
  }   
}