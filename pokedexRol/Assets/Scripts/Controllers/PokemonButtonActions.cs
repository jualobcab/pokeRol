using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class PokemonButtonActions : MonoBehaviour
{
    private pokemons _pokemon;

    public void Initialize(pokemons pokemon)
    {
        _pokemon = pokemon;
    }

    public void ShowDetail()
    {
        Debug.Log($"Has pulsado: {_pokemon.dex_num} - {_pokemon.name}");
        UIManager.Instance.ShowDetails(_pokemon);
    }
}
