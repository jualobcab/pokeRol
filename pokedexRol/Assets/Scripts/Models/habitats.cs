using SQLite;

public class habitats
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    [NotNull, Unique]
    public string name { get; set; }
}