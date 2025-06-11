CREATE SCHEMA `ev_db`;
USE ev_db;

CREATE TABLE `ev_db`.`marca` (
  `id_marca` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_marca`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC) VISIBLE);

CREATE TABLE `ev_db`.`carro` (
  `id_carro` INT NOT NULL AUTO_INCREMENT,
  `id_marca` INT NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `imagen_url` TEXT NULL,
  `fuente_url` TEXT NULL,
  PRIMARY KEY (`id_carro`),
  FOREIGN KEY (`id_marca`) REFERENCES `marca`(`id_marca`),
  INDEX `modelo_idx` (`modelo` ASC) VISIBLE);

CREATE TABLE `ev_db`.`precio` (
  `id_precio` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `pais` ENUM('Alemania', 'Países Bajos', 'Reino Unido') NOT NULL,
  `precio` DECIMAL(15,2) NULL,
  PRIMARY KEY (`id_precio`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`),
  INDEX `pais_idx` (`pais` ASC) VISIBLE);

CREATE TABLE `ev_db`.`especificaciones` (
  `id_especificaciones` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `capacidad_bateria` DECIMAL(5,2) NULL COMMENT 'en kWh',
  `rango_km` INT NULL,
  `eficiencia_whkm` DECIMAL(6,2) NULL,
  `peso_kg` INT NULL,
  `capacidad_remolque_kg` INT NULL,
  PRIMARY KEY (`id_especificaciones`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`));

CREATE TABLE `ev_db`.`carga` (
  `id_carga` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `velocidad_carga_rapida_kw` DECIMAL(5,2) NULL,
  `volumen_carga_l` INT NULL,
  `rango_1_parada_km` INT NULL,
  PRIMARY KEY (`id_carga`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`));

CREATE TABLE `ev_db`.`seguridad` (
  `id_seguridad` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `clasificacion_seguridad` VARCHAR(10) NULL,
  `num_asientos` TINYINT NULL,
  PRIMARY KEY (`id_seguridad`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`));

CREATE TABLE `ev_db`.`equipamiento` (
  `id_equipamiento` INT NOT NULL AUTO_INCREMENT,
  `id_carro` INT NOT NULL,
  `tiene_bomba_calor` BOOLEAN DEFAULT FALSE,
  `tiene_carga_bidireccional` BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (`id_equipamiento`),
  FOREIGN KEY (`id_carro`) REFERENCES `carro`(`id_carro`));