using SQLite;

public class pokemon_hidden_abilities
{
    [PrimaryKey]
    public int pokemon_id { get; set; }
    [PrimaryKey]
    public int ability_id { get; set; }
}
