DROP DATABASE IF EXISTS pokeRol;
CREATE DATABASE pokeRol;
USE pokeRol;

CREATE TABLE `sizes`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `types`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `abilities`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `transformation` BOOLEAN NOT NULL,
    `legendary` BOOLEAN NOT NULL
);

CREATE TABLE `environments`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `pokemons`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `dex_num` BIGINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `size_id` BIGINT UNSIGNED NOT NULL,
    `evasion` VARCHAR(255) NOT NULL,
    `vitality` BIGINT NOT NULL,
    `strength` VARCHAR(255) NOT NULL,
    `agility` VARCHAR(255) NOT NULL,
    `endurance` VARCHAR(255) NOT NULL,
    `mind` VARCHAR(255) NOT NULL,
    `spirit` VARCHAR(255) NOT NULL,
    `presence` VARCHAR(255) NOT NULL,
    `min_level` BIGINT NOT NULL,
    `capture_rate` BIGINT NOT NULL,
    `diet` VARCHAR(255) NULL,
    `sex` VARCHAR(255) NULL,
    `habitat` VARCHAR(255) NULL,
    CONSTRAINT fk_pokemons_size FOREIGN KEY (`size_id`) REFERENCES `sizes`(`id`)
);

CREATE TABLE `pokemon_types`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `type_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`pokemon_id`,`type_id`),
    CONSTRAINT fk_pokemon_types_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_pokemon_types_type FOREIGN KEY (`type_id`) REFERENCES `types`(`id`)
);

CREATE TABLE `proficiencies`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `pokemon_proficiencies`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `proficiency_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`pokemon_id`,`proficiency_id`),
    CONSTRAINT fk_prof_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_prof_proficiency FOREIGN KEY (`proficiency_id`) REFERENCES `proficiencies`(`id`)
);

CREATE TABLE `pokemon_abilities`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `ability_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`pokemon_id`,`ability_id`),
    CONSTRAINT fk_pokemon_abilities_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_pokemon_abilities_ability FOREIGN KEY (`ability_id`) REFERENCES `abilities`(`id`)
);

CREATE TABLE `pokemon_hiddenAbilities`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `ability_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`pokemon_id`,`ability_id`),
    CONSTRAINT fk_hidden_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_hidden_ability FOREIGN KEY (`ability_id`) REFERENCES `abilities`(`id`)
);

CREATE TABLE `pokemon_velocities`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `velocity_id` BIGINT UNSIGNED NOT NULL,
    `quantity` BIGINT NOT NULL,
    PRIMARY KEY (`pokemon_id`,`velocity_id`),
    CONSTRAINT fk_pokemon_vel_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_pokemon_vel_env FOREIGN KEY (`velocity_id`) REFERENCES `environments`(`id`)
);

CREATE TABLE `evolutions`(
    `pokemon_id` BIGINT UNSIGNED NOT NULL,
    `pokemon_evolutionId` BIGINT UNSIGNED NOT NULL,
    `evolution_level` BIGINT NOT NULL,
    `description` VARCHAR(255) NULL,
    PRIMARY KEY (`pokemon_id`,`pokemon_evolutionId`),
    KEY idx_evo_evolutionId (`pokemon_evolutionId`),
    CONSTRAINT fk_evo_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_evo_target FOREIGN KEY (`pokemon_evolutionId`) REFERENCES `pokemons`(`id`)
);

CREATE TABLE `movements`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `type_id` BIGINT UNSIGNED NOT NULL,
    `action` VARCHAR(255) NOT NULL,
    `range` VARCHAR(255) NOT NULL,
    `cost` VARCHAR(255) NOT NULL,
    `associated_stats` VARCHAR(255) NULL,
    `damage` VARCHAR(255) NULL,
    `description` VARCHAR(255) NOT NULL,
    CONSTRAINT fk_mov_type FOREIGN KEY (`type_id`) REFERENCES `types`(`id`)
);

CREATE TABLE `tag`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);

CREATE TABLE `movement_tags`(
    `movement_id` BIGINT UNSIGNED NOT NULL,
    `tag_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (`movement_id`,`tag_id`),
    CONSTRAINT fk_movtag_mov FOREIGN KEY (`movement_id`) REFERENCES `movements`(`id`),
    CONSTRAINT fk_movtag_tag FOREIGN KEY (`tag_id`) REFERENCES `tag`(`id`)
);

CREATE TABLE `moveset_per_level`(
    `pokemon_id` BIGINT UNSIGNED,
    `movement_id` BIGINT UNSIGNED,
    `level` BIGINT,
    KEY idx_mpl_pokemon (`pokemon_id`),
    KEY idx_mpl_movement (`movement_id`),
    CONSTRAINT fk_mpl_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_mpl_movement FOREIGN KEY (`movement_id`) REFERENCES `movements`(`id`)
);

CREATE TABLE `learnset`(
    `pokemon_id` BIGINT UNSIGNED,
    `movement_id` BIGINT UNSIGNED,
    KEY idx_ls_pokemon (`pokemon_id`),
    KEY idx_ls_movement (`movement_id`),
    CONSTRAINT fk_ls_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    CONSTRAINT fk_ls_movement FOREIGN KEY (`movement_id`) REFERENCES `movements`(`id`)
);
