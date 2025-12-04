public class Evolutions
{
    // `pokemon_id` BIGINT UNSIGNED NOT NULL,
    //     `pokemon_evolutionId` BIGINT UNSIGNED NOT NULL,
    //     `evolution_level` BIGINT NOT NULL,
    // `description` VARCHAR(255) NULL,
    // PRIMARY KEY (`pokemon_id`,`pokemon_evolutionId`),
    // KEY idx_evo_evolutionId (`pokemon_evolutionId`),
    // CONSTRAINT fk_evo_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    // CONSTRAINT fk_evo_target FOREIGN KEY (`pokemon_evolutionId`) REFERENCES `pokemons`(`id`)
}
