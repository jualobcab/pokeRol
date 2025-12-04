public class Pokemon_velocities
{
    // `pokemon_id` BIGINT UNSIGNED NOT NULL,
    //     `velocity_id` BIGINT UNSIGNED NOT NULL,
    //     `quantity` BIGINT NOT NULL,
    // PRIMARY KEY (`pokemon_id`,`velocity_id`),
    // CONSTRAINT fk_pokemon_vel_pokemon FOREIGN KEY (`pokemon_id`) REFERENCES `pokemons`(`id`),
    // CONSTRAINT fk_pokemon_vel_env FOREIGN KEY (`velocity_id`) REFERENCES `environments`(`id`)
}
