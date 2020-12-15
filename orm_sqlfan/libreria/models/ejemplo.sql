SELECT "libreria_libro"."isbn",
       "libreria_libro"."titulo",
       "libreria_libro"."categoria",
        ...
       "libreria_editorial"."id",
       "libreria_editorial"."nombre"
  FROM "libreria_libro"
 INNER JOIN "libreria_editorial"
    ON ("libreria_libro"."editorial_id" = "libreria_editorial"."id")
 WHERE UPPER("libreria_libro"."categoria"::text) LIKE UPPER('%python%')

