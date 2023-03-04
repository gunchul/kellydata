-- MySQL Script generated by MySQL Workbench
-- Sat Mar  4 17:22:02 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema kellydata
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema kellydata
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `kellydata` DEFAULT CHARACTER SET utf8 ;
USE `kellydata` ;

-- -----------------------------------------------------
-- Table `kellydata`.`rba_price`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kellydata`.`rba_price` (
  `added_date` DATETIME NULL,
  `date` DATETIME NOT NULL,
  `price` DOUBLE NOT NULL,
  `changed_rate` DOUBLE NOT NULL,
  PRIMARY KEY (`date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kellydata`.`auction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kellydata`.`auction` (
  `added_date` DATETIME NULL,
  `date` DATETIME NOT NULL,
  `city` VARCHAR(128) NOT NULL,
  `total_auctions` INT NULL,
  `sold_prior_to_auction` INT NULL,
  `sold_at_auction` INT NULL,
  `sold_after_auction` INT NULL,
  `passed_in` INT NULL,
  `withdrawn` INT NULL,
  `clearance_rate` DOUBLE NULL,
  `cleared_auctions` INT NULL,
  `uncleared_auctions` INT NULL,
  PRIMARY KEY (`date`, `city`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
