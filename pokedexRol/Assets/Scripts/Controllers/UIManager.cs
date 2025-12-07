using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;

public class UIManager : MonoBehaviour
{
    public static UIManager Instance;

    [Header("Panels")]
    public GameObject mainPanel;
    public GameObject detailsPanel;

    [Header("Detail UI")]
    public TMP_Text pokemonName;
    public TMP_Text dexNum;

    void Awake()
    {
        Instance = this;
        detailsPanel.SetActive(false); // Oculto al inicio
    }

    public void ShowDetails(pokemons pokemon)
    {
        TMP_Text[] texts = detailsPanel.GetComponentsInChildren<TMP_Text>();
        foreach (var txt in texts)
        {
            Debug.Log(txt.name);
            switch (txt.name)
            {
                case "Name":
                    txt.text = pokemon.name;
                    break;
                case "DexNum":
                    txt.text = $"#{pokemon.dex_num:D4}";
                    break;
                case "FueValue":
                    txt.text = pokemon.strength.Replace('☆','*').Replace("★","**");
                    break;
                case "AgiValue":
                    txt.text = pokemon.agility.Replace('☆','*').Replace("★","**");
                    break;
                case "ResValue":
                    txt.text = pokemon.endurance.Replace('☆','*').Replace("★","**");
                    break;
                case "MenValue":
                    txt.text = pokemon.mind.Replace('☆','*').Replace("★","**");
                    break;
                case "EspValue":
                    txt.text = pokemon.spirit.Replace('☆','*').Replace("★","**");
                    break;
                case "PreValue":
                    txt.text = pokemon.presence.Replace('☆','*').Replace("★","**");
                    break;
            }
        }

        StartCoroutine(AnimatePanels(mainPanel, detailsPanel));
    }

    public void BackToMain()
    {
        StartCoroutine(AnimatePanels(detailsPanel, mainPanel));
    }

    /// Animación simple tipo Fade o Slide
    IEnumerator AnimatePanels(GameObject from, GameObject to)
    {
        RectTransform a = from.GetComponent<RectTransform>();
        RectTransform b = to.GetComponent<RectTransform>();

        Vector2 offRight = new Vector2(Screen.width, 0);
        Vector2 offLeft = new Vector2(-Screen.width, 0);

        b.anchoredPosition = offRight; 
        to.SetActive(true);

        float t = 0;
        while (t < 0.3f)
        {
            t += Time.deltaTime;
            float v = t / 0.3f;

            a.anchoredPosition = Vector2.Lerp(Vector2.zero, offLeft, v);
            b.anchoredPosition = Vector2.Lerp(offRight, Vector2.zero, v);

            yield return null;
        }

        from.SetActive(false);
    }

}