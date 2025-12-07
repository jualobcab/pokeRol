using SQLite;

public class evolutions
{
    [PrimaryKey, NotNull]
    public int pokemon_id { get; set; }
    [PrimaryKey, NotNull]
    public int pokemon_evolution_id { get; set; }
    [NotNull]
    public int evolution_level { get; set; }
    public string extra_requisites { get; set; }
}
