using SQLite;
public class pokemons
{
    [PrimaryKey, AutoIncrement]
    public int id { get; set; }
    public int dex_num  { get; set; }
    public string name { get; set; }
    public int size_id { get; set; }
    public string evasion { get; set; }
    public int vitality { get; set; }
    public string strength { get; set; }
    public string agility { get; set; }
    public string endurance { get; set; }
    public string mind { get; set; }
    public string spirit { get; set; }
    public string presence { get; set; }
    public int min_level { get; set; }
    public int capture_rate { get; set; }
    public string diet { get; set; }
    public string sex { get; set; }
}
