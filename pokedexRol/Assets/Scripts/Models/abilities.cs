using SQLite;

public class abilities
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    [NotNull]
    public string name { get; set; }
    [NotNull]
    public string description { get; set; }
    [NotNull]
    public bool transformation { get; set; }
    [NotNull]
    public bool legendary { get; set; }
}
