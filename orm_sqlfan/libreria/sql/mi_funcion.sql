CREATE OR REPLACE FUNCTION mi_funcion(buscar varchar(50)) 
RETURNS TABLE(id int,nombre varchar(100)) 
AS $$
BEGIN
RETURN QUERY
    SELECT a.id,a.nombre 
	FROM libreria_editorial as a
	WHERE buscar = CASE WHEN buscar='todos' then buscar else a.nombre END;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION mi_funcion_out(buscar varchar(50),out resultado json,out saludo varchar(10)) 
AS $$
BEGIN
     resultado=array_to_json(array_agg(row_to_json(t)))
	from (
		 SELECT a.id,a.nombre 
		 FROM libreria_editorial as a
		 WHERE buscar = CASE WHEN buscar='todos' then buscar else a.nombre END	
	) t;
	saludo='Hola mundo';
END;
$$ LANGUAGE plpgsql;