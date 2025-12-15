PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS abilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    transformation BOOLEAN NOT NULL,
    legendary BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS environments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dex_num INTEGER NOT NULL,
    name TEXT NOT NULL,
    size_id INTEGER NOT NULL,
    evasion TEXT NOT NULL,
    vitality TEXT NOT NULL,
    strength TEXT NOT NULL,
    agility TEXT NOT NULL,
    endurance TEXT NOT NULL,
    mind TEXT NOT NULL,
    spirit TEXT NOT NULL,
    presence TEXT NOT NULL,
    min_level INTEGER NOT NULL,
    capture_rate INTEGER NOT NULL,
    diet TEXT,
    sex TEXT,
    sex_differences INTEGER NOT NULL DEFAULT 0,
    different_forms INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    FOREIGN KEY(size_id) REFERENCES sizes(id)
);

CREATE TABLE IF NOT EXISTS pokemon_types (
    pokemon_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(type_id) REFERENCES types(id)
);

CREATE TABLE IF NOT EXISTS proficiencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemon_proficiencies (
    pokemon_id INTEGER NOT NULL,
    proficiency_id INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, proficiency_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(proficiency_id) REFERENCES proficiencies(id)
);

CREATE TABLE IF NOT EXISTS pokemon_abilities (
    pokemon_id INTEGER NOT NULL,
    ability_id INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(ability_id) REFERENCES abilities(id)
);

CREATE TABLE IF NOT EXISTS pokemon_hidden_abilities (
    pokemon_id INTEGER NOT NULL,
    ability_id INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(ability_id) REFERENCES abilities(id)
);

CREATE TABLE IF NOT EXISTS pokemon_velocities (
    pokemon_id INTEGER NOT NULL,
    environment_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, environment_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(environment_id) REFERENCES environments(id)
);

CREATE TABLE IF NOT EXISTS evolutions (
    pokemon_id INTEGER NOT NULL,
    pokemon_evolution_id INTEGER NOT NULL,
    evolution_level INTEGER NOT NULL,
    extra_requisites TEXT,
    PRIMARY KEY (pokemon_id, pokemon_evolution_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(pokemon_evolution_id) REFERENCES pokemons(id)
);

CREATE TABLE IF NOT EXISTS movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    type_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    range TEXT NOT NULL,
    cost TEXT NOT NULL,
    associated_stats TEXT,
    damage TEXT,
    description TEXT NOT NULL,
    FOREIGN KEY(type_id) REFERENCES types(id)
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS movement_tags (
    movement_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (movement_id, tag_id),
    FOREIGN KEY(movement_id) REFERENCES movements(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);

CREATE TABLE IF NOT EXISTS moveset_per_level (
    pokemon_id INTEGER,
    movement_id INTEGER,
    level INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(movement_id) REFERENCES movements(id)
);

CREATE TABLE IF NOT EXISTS learnset (
    pokemon_id INTEGER,
    movement_id INTEGER,
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(movement_id) REFERENCES movements(id)
);

CREATE TABLE IF NOT EXISTS senses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemon_senses (
    pokemon_id INTEGER NOT NULL,
    sense_id INTEGER NOT NULL,
    quantity TEXT,
    PRIMARY KEY (pokemon_id, sense_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(sense_id) REFERENCES senses(id)
);

CREATE TABLE IF NOT EXISTS habitats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemon_habitats (
    pokemon_id INTEGER NOT NULL,
    habitat_id INTEGER NOT NULL,
    PRIMARY KEY (pokemon_id, habitat_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemons(id),
    FOREIGN KEY(habitat_id) REFERENCES habitats(id)
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type INTEGER NOT NULL,
    rarity TEXT CHECK(rarity IN ('Común', 'Poco común', 'Raro', 'Muy raro', 'Insólito')) NOT NULL,
    cost TEXT,
    description TEXT NOT NULL,
    FOREIGN KEY(type) REFERENCES item_types(item_id)
);

CREATE TABLE IF NOT EXISTS item_types (
    item_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL    
);