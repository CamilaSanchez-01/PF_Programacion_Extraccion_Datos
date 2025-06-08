CREATE SCHEMA `ev_db` ;
USE ev_db;


CREATE TABLE `ev_db`.`marca` (
  `id_marca` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_marca`));
  
CREATE TABLE `ev_db`.`carro` (
  `id_carro` INT NOT NULL AUTO_INCREMENT,
  `id_marca` INT NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `imagen_url` TEXT NULL,
  `fuente_url` TEXT NULL,
  PRIMARY KEY (`id_carro`),
  FOREIGN KEY (`id_marca`) REFERENCES `marca`(`id_marca`)
    );
    
CREATE TABLE `ev_db`.`precio` (
  `id_precio` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `pais` VARCHAR(55) NOT NULL,
  `precio` DECIMAL(10,6) NULL,
  PRIMARY KEY (`id_precio`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)
  );
  
CREATE TABLE `ev_db`.`bateria` (
  `id_bateria` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NULL,
  `capacidad` VARCHAR(55) NULL,
  PRIMARY KEY (`id_bateria`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)
  );

CREATE TABLE `ev_db`.`rendimiento` (
  `id_rendimiento` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `rango_km` VARCHAR(50) NULL,
  `eficiencia` VARCHAR(50) NULL,
  `peso` VARCHAR(50) NULL,
  PRIMARY KEY (`id_rendimiento`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)  
  );

CREATE TABLE `ev_db`.`carga` (
  `id_carga` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `carga_rapida_kw` VARCHAR(50) NULL,
  `volumen_carga_l` VARCHAR(50) NULL,
  `rango_1_parada_km` VARCHAR(50) NULL,
  PRIMARY KEY (`id_carga`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)    
  );

CREATE TABLE `ev_db`.`traccion` (
  `id_traccion` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `trasera` VARCHAR(55) NULL,
  `delantera` VARCHAR(55) NULL,
  PRIMARY KEY (`id_traccion`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)      
  );
  
CREATE TABLE `ev_db`.`seguridad` (
  `id_seguridad` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `clasificacion_seguridad` VARCHAR(55) NULL,
  PRIMARY KEY (`id_seguridad`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)      
  );

CREATE TABLE `ev_db`.`asientos` (
  `id_asientos` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `cantidad` VARCHAR(15) NULL,
  PRIMARY KEY (`id_asientos`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)      
  );

CREATE TABLE `ev_db`.`extras` (
  `id_extras` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `bomba_calor` VARCHAR(55) NULL,
  `carga_bidireccional` VARCHAR(65) NULL,
  PRIMARY KEY (`id_extras`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)      
  );

CREATE TABLE `ev_db`.`segmento` (
  `id_segmento` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NULL,
  `tipo_segmento` VARCHAR(65) NULL,
  PRIMARY KEY (`id_segmento`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`)      
  );