using SQLite;

public class moveset_per_level
{
    [PrimaryKey]
    public int pokemon_id { get; set; }
    [PrimaryKey]
    public int movement_id { get; set; }
    public int level { get; set; }
}
