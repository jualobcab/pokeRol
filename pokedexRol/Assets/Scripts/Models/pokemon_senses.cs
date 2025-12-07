using SQLite;

public class pokemon_senses
{
    [PrimaryKey]
    public int pokemon_id { get; set; }
    [PrimaryKey]
    public int ability_id { get; set; }
    public string quantity { get; set; }
}