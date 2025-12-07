using SQLite;

public class pokemon_velocities
{
    [PrimaryKey]
    public int pokemon_id { get; set; }
    [PrimaryKey]
    public int ability_id { get; set; }
    [NotNull]
    public int quantity { get; set; }
}
