using UnityEngine;
using UnityEngine.UI;

public class PokemonButtonActions : MonoBehaviour
{
    private DatabaseController _dbLoader;
    private PokemonDetail _pokemon;
    
    public void Initialize(pokemons pokemon)
    {
        _dbLoader = DatabaseController.Instance;
        _pokemon = new PokemonDetail();
        _pokemon.name = pokemon.name;
        _pokemon.dex_num = pokemon.dex_num;
        _pokemon.size_id = pokemon.dex_num;
        _pokemon.evasion = pokemon.evasion;
        _pokemon.vitality = pokemon.vitality;
        _pokemon.strength = pokemon.strength;
        _pokemon.agility = pokemon.agility;
        _pokemon.endurance = pokemon.endurance;
        _pokemon.mind = pokemon.mind;
        _pokemon.spirit = pokemon.spirit;
        _pokemon.presence = pokemon.presence;
        _pokemon.min_level = pokemon.min_level;
        _pokemon.capture_rate = pokemon.capture_rate;
        _pokemon.diet = pokemon.diet;
        _pokemon.sex = pokemon.sex;

        _pokemon.types = _dbLoader.LoadPokemonTypes(pokemon.id);
    }

    public void ShowDetail()
    {
        Debug.Log($"Has pulsado: {_pokemon.dex_num} - {_pokemon.name}");
        
        UIManager.Instance.ShowDetails(_pokemon);
    }
}
