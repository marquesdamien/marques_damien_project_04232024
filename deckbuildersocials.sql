-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema deckbuildersocials
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `deckbuildersocials` ;

-- -----------------------------------------------------
-- Schema deckbuildersocials
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `deckbuildersocials` DEFAULT CHARACTER SET utf8 ;
USE `deckbuildersocials` ;

-- -----------------------------------------------------
-- Table `deckbuildersocials`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `deckbuildersocials`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password` VARCHAR(355) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `id_UNIQUE` (`user_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `deckbuildersocials`.`decks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `deckbuildersocials`.`decks` (
  `deck_id` INT NOT NULL AUTO_INCREMENT,
  `deck_name` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  `decktype` TINYINT NOT NULL,
  PRIMARY KEY (`deck_id`, `user_id`),
  UNIQUE INDEX `id_UNIQUE` (`deck_id` ASC) VISIBLE,
  INDEX `fk_decks_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_decks_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `deckbuildersocials`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `deckbuildersocials`.`userbookcomments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `deckbuildersocials`.`userbookcomments` (
  `comment_id` INT NOT NULL,
  `decks_id` INT NOT NULL,
  `decks_user_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `comment` TEXT(80) NOT NULL,
  PRIMARY KEY (`comment_id`, `decks_id`, `decks_user_id`, `user_id`),
  UNIQUE INDEX `id_UNIQUE` (`comment_id` ASC) VISIBLE,
  INDEX `fk_userbookcomments_decks1_idx` (`decks_id` ASC, `decks_user_id` ASC) VISIBLE,
  INDEX `fk_userbookcomments_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_userbookcomments_decks1`
    FOREIGN KEY (`decks_id` , `decks_user_id`)
    REFERENCES `deckbuildersocials`.`decks` (`deck_id` , `user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_userbookcomments_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `deckbuildersocials`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `deckbuildersocials`.`cards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `deckbuildersocials`.`cards` (
  `cards_id` INT NOT NULL AUTO_INCREMENT,
  `card_name` VARCHAR(255) NOT NULL,
  `decks_id` INT NOT NULL,
  `decks_user_id` INT NOT NULL,
  PRIMARY KEY (`cards_id`, `decks_id`, `decks_user_id`),
  UNIQUE INDEX `idcards_UNIQUE` (`cards_id` ASC) VISIBLE,
  INDEX `fk_cards_decks1_idx` (`decks_id` ASC, `decks_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_cards_decks1`
    FOREIGN KEY (`decks_id` , `decks_user_id`)
    REFERENCES `deckbuildersocials`.`decks` (`deck_id` , `user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
