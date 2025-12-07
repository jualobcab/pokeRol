using SQLite;

public class tag
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    public string name { get; set; }
}
