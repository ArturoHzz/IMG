-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema img
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema img
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `img` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `img` ;

-- -----------------------------------------------------
-- Table `img`.`perfil`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`perfil` (
  `idPerfil` INT NOT NULL,
  `nombre_perfil` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idPerfil`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`serie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`serie` (
  `idSerie` INT NOT NULL,
  `nombre_serie` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idSerie`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`color`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`color` (
  `idColor` INT NOT NULL,
  `nombre_color` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idColor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`aluminio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`aluminio` (
  `idAluminio` INT NOT NULL,
  `idPerfil` INT NULL DEFAULT NULL,
  `idSerie` INT NULL DEFAULT NULL,
  `idColor` INT NULL DEFAULT NULL,
  `largo` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idAluminio`),
  INDEX `idPerfil` (`idPerfil` ASC) VISIBLE,
  INDEX `idSerie` (`idSerie` ASC) VISIBLE,
  INDEX `idColor` (`idColor` ASC) VISIBLE,
  CONSTRAINT `aluminio_ibfk_1`
    FOREIGN KEY (`idPerfil`)
    REFERENCES `img`.`perfil` (`idPerfil`),
  CONSTRAINT `aluminio_ibfk_2`
    FOREIGN KEY (`idSerie`)
    REFERENCES `img`.`serie` (`idSerie`),
  CONSTRAINT `aluminio_ibfk_3`
    FOREIGN KEY (`idColor`)
    REFERENCES `img`.`color` (`idColor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`bisagras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`bisagras` (
  `idBisagras` INT NOT NULL,
  `tipo_bisagra` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idBisagras`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`carretas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`carretas` (
  `idCarretas` INT NOT NULL,
  `nombre_carretas` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idCarretas`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`chapa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`chapa` (
  `idChapa` INT NOT NULL,
  `tipo_chapa` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idChapa`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`compra` (
  `idCompra` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `proveedor` VARCHAR(100) NULL DEFAULT NULL,
  `observaciones` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idCompra`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`espesor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`espesor` (
  `idEspesor` INT NOT NULL,
  `medida_mm` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idEspesor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`tipo_cristal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`tipo_cristal` (
  `idTipo_cristal` INT NOT NULL,
  `nombre_tipo` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idTipo_cristal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`cristal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`cristal` (
  `idCristal` INT NOT NULL,
  `idEspesor` INT NULL DEFAULT NULL,
  `idTipo_cristal` INT NULL DEFAULT NULL,
  `idColor` INT NULL DEFAULT NULL,
  `tipo_hoja` ENUM('media', 'chica', 'grande') NULL,
  `descripcion` VARCHAR(45) NULL,
  PRIMARY KEY (`idCristal`),
  INDEX `idEspesor` (`idEspesor` ASC) VISIBLE,
  INDEX `idTipo_cristal` (`idTipo_cristal` ASC) VISIBLE,
  INDEX `idColor` (`idColor` ASC) VISIBLE,
  CONSTRAINT `cristal_ibfk_1`
    FOREIGN KEY (`idEspesor`)
    REFERENCES `img`.`espesor` (`idEspesor`),
  CONSTRAINT `cristal_ibfk_2`
    FOREIGN KEY (`idTipo_cristal`)
    REFERENCES `img`.`tipo_cristal` (`idTipo_cristal`),
  CONSTRAINT `cristal_ibfk_3`
    FOREIGN KEY (`idColor`)
    REFERENCES `img`.`color` (`idColor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_compra_aluminio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_compra_aluminio` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idCompra` INT NULL DEFAULT NULL,
  `idAluminio` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  `precio_unitario` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idCompra` (`idCompra` ASC) VISIBLE,
  INDEX `idAluminio` (`idAluminio` ASC) VISIBLE,
  CONSTRAINT `detalle_compra_aluminio_ibfk_1`
    FOREIGN KEY (`idCompra`)
    REFERENCES `img`.`compra` (`idCompra`),
  CONSTRAINT `detalle_compra_aluminio_ibfk_2`
    FOREIGN KEY (`idAluminio`)
    REFERENCES `img`.`aluminio` (`idAluminio`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_compra_cristal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_compra_cristal` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idCompra` INT NULL DEFAULT NULL,
  `idCristal` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  `precio_unitario` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idCompra` (`idCompra` ASC) VISIBLE,
  INDEX `idCristal` (`idCristal` ASC) VISIBLE,
  CONSTRAINT `detalle_compra_cristal_ibfk_1`
    FOREIGN KEY (`idCompra`)
    REFERENCES `img`.`compra` (`idCompra`),
  CONSTRAINT `detalle_compra_cristal_ibfk_2`
    FOREIGN KEY (`idCristal`)
    REFERENCES `img`.`cristal` (`idCristal`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`jaladeras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`jaladeras` (
  `idJaladeras` INT NOT NULL,
  `tipo_jaladeras` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`idJaladeras`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`herrajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`herrajes` (
  `idHerrajes` INT NOT NULL,
  `idCarretas` INT NULL DEFAULT NULL,
  `idJaladeras` INT NULL DEFAULT NULL,
  `idChapa` INT NULL DEFAULT NULL,
  `idBisagras` INT NULL DEFAULT NULL,
  `idColor` INT NULL DEFAULT NULL,
  PRIMARY KEY (`idHerrajes`),
  INDEX `idCarretas` (`idCarretas` ASC) VISIBLE,
  INDEX `idJaladeras` (`idJaladeras` ASC) VISIBLE,
  INDEX `idChapa` (`idChapa` ASC) VISIBLE,
  INDEX `idBisagras` (`idBisagras` ASC) VISIBLE,
  INDEX `idColor` (`idColor` ASC) VISIBLE,
  CONSTRAINT `herrajes_ibfk_1`
    FOREIGN KEY (`idCarretas`)
    REFERENCES `img`.`carretas` (`idCarretas`),
  CONSTRAINT `herrajes_ibfk_2`
    FOREIGN KEY (`idJaladeras`)
    REFERENCES `img`.`jaladeras` (`idJaladeras`),
  CONSTRAINT `herrajes_ibfk_3`
    FOREIGN KEY (`idChapa`)
    REFERENCES `img`.`chapa` (`idChapa`),
  CONSTRAINT `herrajes_ibfk_4`
    FOREIGN KEY (`idBisagras`)
    REFERENCES `img`.`bisagras` (`idBisagras`),
  CONSTRAINT `herrajes_ibfk_5`
    FOREIGN KEY (`idColor`)
    REFERENCES `img`.`color` (`idColor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_compra_herrajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_compra_herrajes` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idCompra` INT NULL DEFAULT NULL,
  `idHerrajes` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  `precio_unitario` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idCompra` (`idCompra` ASC) VISIBLE,
  INDEX `idHerrajes` (`idHerrajes` ASC) VISIBLE,
  CONSTRAINT `detalle_compra_herrajes_ibfk_1`
    FOREIGN KEY (`idCompra`)
    REFERENCES `img`.`compra` (`idCompra`),
  CONSTRAINT `detalle_compra_herrajes_ibfk_2`
    FOREIGN KEY (`idHerrajes`)
    REFERENCES `img`.`herrajes` (`idHerrajes`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`salida`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`salida` (
  `idSalida` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `motivo` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idSalida`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_salida_aluminio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_salida_aluminio` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idSalida` INT NULL DEFAULT NULL,
  `idAluminio` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idSalida` (`idSalida` ASC) VISIBLE,
  INDEX `idAluminio` (`idAluminio` ASC) VISIBLE,
  CONSTRAINT `detalle_salida_aluminio_ibfk_1`
    FOREIGN KEY (`idSalida`)
    REFERENCES `img`.`salida` (`idSalida`),
  CONSTRAINT `detalle_salida_aluminio_ibfk_2`
    FOREIGN KEY (`idAluminio`)
    REFERENCES `img`.`aluminio` (`idAluminio`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_salida_cristal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_salida_cristal` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idSalida` INT NULL DEFAULT NULL,
  `idCristal` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idSalida` (`idSalida` ASC) VISIBLE,
  INDEX `idCristal` (`idCristal` ASC) VISIBLE,
  CONSTRAINT `detalle_salida_cristal_ibfk_1`
    FOREIGN KEY (`idSalida`)
    REFERENCES `img`.`salida` (`idSalida`),
  CONSTRAINT `detalle_salida_cristal_ibfk_2`
    FOREIGN KEY (`idCristal`)
    REFERENCES `img`.`cristal` (`idCristal`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`detalle_salida_herrajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`detalle_salida_herrajes` (
  `idDetalle` INT NOT NULL AUTO_INCREMENT,
  `idSalida` INT NULL DEFAULT NULL,
  `idHerrajes` INT NULL DEFAULT NULL,
  `cantidad` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`idDetalle`),
  INDEX `idSalida` (`idSalida` ASC) VISIBLE,
  INDEX `idHerrajes` (`idHerrajes` ASC) VISIBLE,
  CONSTRAINT `detalle_salida_herrajes_ibfk_1`
    FOREIGN KEY (`idSalida`)
    REFERENCES `img`.`salida` (`idSalida`),
  CONSTRAINT `detalle_salida_herrajes_ibfk_2`
    FOREIGN KEY (`idHerrajes`)
    REFERENCES `img`.`herrajes` (`idHerrajes`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`stock_aluminio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`stock_aluminio` (
  `idAluminio` INT NOT NULL,
  `cantidad` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`idAluminio`),
  CONSTRAINT `stock_aluminio_ibfk_1`
    FOREIGN KEY (`idAluminio`)
    REFERENCES `img`.`aluminio` (`idAluminio`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`stock_cristal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`stock_cristal` (
  `idCristal` INT NOT NULL,
  `cantidad` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`idCristal`),
  CONSTRAINT `stock_cristal_ibfk_1`
    FOREIGN KEY (`idCristal`)
    REFERENCES `img`.`cristal` (`idCristal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `img`.`stock_herrajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `img`.`stock_herrajes` (
  `idHerrajes` INT NOT NULL,
  `cantidad` DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`idHerrajes`),
  CONSTRAINT `stock_herrajes_ibfk_1`
    FOREIGN KEY (`idHerrajes`)
    REFERENCES `img`.`herrajes` (`idHerrajes`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
