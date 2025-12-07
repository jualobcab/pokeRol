using SQLite;

public class environments
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    [NotNull]
    public string name { get; set; }
}
