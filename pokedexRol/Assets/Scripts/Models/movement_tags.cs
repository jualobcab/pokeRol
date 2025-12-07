using SQLite;

public class movement_tags
{
    [PrimaryKey, NotNull]
    public int movement_id { get; set; }
    [PrimaryKey, NotNull]
    public int tag_id { get; set; }
}
