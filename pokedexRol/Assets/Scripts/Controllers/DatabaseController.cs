using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using SQLite;
using UnityEditor;

public class DatabaseController : MonoBehaviour
{
    public static DatabaseController Instance;
    private SQLiteConnection db;
    void Awake()
    {
        if (Instance == null)
            Instance = this;
        else
            Destroy(this);
    }
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        string dbPath = InstallDB("pokeRol.db");
        db = new SQLiteConnection(dbPath);

        Debug.Log("DB cargada desde: " + dbPath);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public static string InstallDB(string fileName)
    {
        string persistentPath = Path.Combine(Application.persistentDataPath, fileName);
        string streamingPath = Path.Combine(Application.streamingAssetsPath, fileName);

        // Si ya existe en persistentDataPath, usar esa
        if (File.Exists(persistentPath))
            persistentPath.Remove(0);

        // ANDROID requiere WWW para leer StreamingAssets
        if (Application.platform == RuntimePlatform.Android)
        {
            // Leer binario desde dentro del APK
            var www = UnityEngine.Networking.UnityWebRequest.Get(streamingPath);
            www.SendWebRequest();
            while (!www.isDone) { }

            if (www.result != UnityEngine.Networking.UnityWebRequest.Result.Success)
                throw new System.Exception("Error copiando base de datos: " + www.error);

            File.WriteAllBytes(persistentPath, www.downloadHandler.data);
        }
        else
        {
            // PC/Mac/iOS puede copiar directamente
            File.Copy(streamingPath, persistentPath, true);
        }

        return persistentPath;
    }
    
    public List<pokemons> LoadPokemons()
    {
        return db.Table<pokemons>().ToList();
    }

    public List<types> LoadPokemonTypes(int pokemonId)
    {
        string query = @"
        SELECT t.*
        FROM types t
        JOIN pokemon_types pt ON t.id = pt.type_id
        WHERE pt.pokemon_id = ?";

        return db.Query<types>(query, pokemonId);
    }
}
