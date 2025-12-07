using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro; // Si usas TextMeshPro

public class MainGridButtons : MonoBehaviour
{
    public DatabaseController dbLoader;
    public Transform gridParent;           // Content del ScrollView
    public GameObject buttonPrefab;        // Un botón base

    void Start()
    {
        List<pokemons> items = dbLoader.LoadPokemons();
        GenerateGrid(items);
    }

    void GenerateGrid(List<pokemons> pokemons)
    {
        foreach (var pokemon in pokemons)
        {
            GameObject btnObj = Instantiate(buttonPrefab, gridParent);
            Button btn = btnObj.GetComponent<Button>();

            TMP_Text[] txts = btnObj.GetComponentsInChildren<TMP_Text>();
            foreach (var txt in txts)
            {
                //Debug.Log(txt.name);
                switch (txt.name)
                {
                    case "Name":
                        txt.text = pokemon.name;
                        break;
                    case "dex_num":
                        txt.text = $"#{pokemon.dex_num:D4}";
                        break;
                }
            }

            // Evento del botón
            btn.GetComponent<PokemonButtonActions>().Initialize(pokemon);
            btn.onClick.AddListener(() => btn.GetComponent<PokemonButtonActions>().ShowDetail());
        }
    }
}