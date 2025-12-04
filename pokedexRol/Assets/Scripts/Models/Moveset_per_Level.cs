public class Moveset_per_Level
{
    // `pokemon_id` BIGINT UNSIGNED,
    //     `movement_id` BIGINT UNSIGNED,
    //     `level` BIGINT,
    // KEY idx_mpl_pokemon (`pokemon_id`),
    // KEY idx_mpl_movement (`movement_id`),
    // CONSTRAINT fk_mpl_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    // CONSTRAINT fk_mpl_movement FOREIGN KEY (`movement_id`) REFERENCES `movements`(`id`)
}
