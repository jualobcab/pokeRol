using SQLite;

public class movements
{
    [PrimaryKey, NotNull]
    public int id { get; set; }
    [NotNull]
    public int type_id { get; set; }
    [NotNull]
    public string action { get; set; }
    [NotNull]
    public string range { get; set; }
    [NotNull]
    public string cost { get; set; }
    public string associated_stats { get; set; }
    public string damage { get; set; }
    [NotNull]
    public string description { get; set; }
}
