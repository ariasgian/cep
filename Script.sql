create  database corte;


 corte;

CREATE TABLE public.altura
(
    id serial,
    maquina character(4) NOT NULL,
    tipo character(30) NOT NULL,
    cable character(20) NOT NULL,
    terminal character(20) NOT NULL,
    altura double precision NOT NULL,
    fecha date NOT null,
    PRIMARY KEY (id)
);


select * from altura a ;

Insert into altura(maquina, tipo, cable, terminal, altura, fecha) values(2,'test','abc122', '1212j',1.5,'2021-05-21');

truncate altura;

CREATE TABLE public.cable
(
    pn varchar(20) NOT NULL,
    seccion double precision NOT NULL,
    PRIMARY KEY (pn)
);

truncate validacion;

CREATE TABLE public.validacion
(
    id varchar(20) NOT NUlL,
    terminal varchar(20) NOT NULL,
    seccion double precision NOT NULL,
    cch double precision NOT NULL,
    ich double precision NOT NULL,
    PRIMARY KEY (id)
);

select * from validacion;


select id, cable,terminal, altura from public.altura 
where tipo= 'MEASUREMENT_DATA_IH_2';
