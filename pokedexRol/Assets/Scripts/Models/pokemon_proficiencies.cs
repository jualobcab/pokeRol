using SQLite;

public class pokemon_proficiencies
{
    [PrimaryKey]
    public int pokemon_id { get; set; }
    [PrimaryKey]
    public int ability_id { get; set; }
}
