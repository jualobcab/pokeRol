using SQLite;

public class types
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    public string name { get; set; }
}
