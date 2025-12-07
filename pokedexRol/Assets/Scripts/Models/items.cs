using SQLite;

public class items
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    [Unique, NotNull]
    public string name { get; set; }
    [NotNull]
    public string type { get; set; }
    [NotNull]
    public string rarity { get; set; }
    public int cost { get; set; }
    [NotNull]
    public string description { get; set; }
}