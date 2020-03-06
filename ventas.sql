create table producto
(
	cod_producto int auto_increment
		primary key,
	nombre       varchar(100) not null,
	descripcion  varchar(500) null
);

create table vendedor
(
	cod_vendedor     int auto_increment
		primary key,
	nombre           varchar(100) not null,
	salario          float        null,
	fecha_nacimiento date         not null
);

create table venta
(
	cod_venta   int auto_increment
		primary key,
	costo       float    not null,
	fk_producto int      not null,
	fk_vendedor int      not null,
	fecha_hora  datetime not null,
	constraint venta___fk_producto
		foreign key (fk_producto) references producto (cod_producto),
	constraint venta___fk_vendedor
		foreign key (fk_vendedor) references vendedor (cod_vendedor)
);


