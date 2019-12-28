DROP VIEW IF EXISTS v_libroautores;


create view v_libroautores as
    select lib.isbn as id, lib.isbn,lib.titulo,
    GROUP_CONCAT(aut.nombre) as Autores
    from libreria_libro as  lib
    left join libreria_autorcapitulo as rel
    on rel.libro_id = lib.isbn
    left join libreria_autor as aut
    on aut.id = rel.autor_id
    group by lib.isbn,lib.titulo

