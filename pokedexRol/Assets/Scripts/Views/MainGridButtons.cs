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

    void GenerateGrid(List<pokemons> items)
    {
        foreach (var item in items)
        {
            GameObject btnObj = Instantiate(buttonPrefab, gridParent);
            Button btn = btnObj.GetComponent<Button>();

            TMP_Text[] txts = btnObj.GetComponentsInChildren<TMP_Text>();
            foreach (var txt in txts)
            {
                Debug.Log(txt.name);
                switch (txt.name)
                {
                    case "Name":
                        txt.text = item.name;
                        break;
                    case "dex_num":
                        txt.text = $"#{item.dex_num:D4}";
                        break;
                }
            //txt.text = item.name;
            }

            // Evento del botón
            btn.onClick.AddListener(() => OnItemClick(item));
        }
    }

    void OnItemClick(pokemons item)
    {
        Debug.Log($"Has pulsado: {item.dex_num} - {item.name}");
    }
}