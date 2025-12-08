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

    [Header("TypesPanel")] 
    public Transform typesPanel;
    public GameObject typePrefab;

    void Awake()
    {
        Instance = this;
        detailsPanel.SetActive(false); // Oculto al inicio
    }

    public void ShowDetails(PokemonDetail pokemon)
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

        foreach (var type in pokemon.types)
        {
            var btnObj = Instantiate(typePrefab, typesPanel);
            // Obtener referencia al script del prefab
            var buttonItem = btnObj.GetComponent<TypeButton>();
            // Determinar color según el texto
            Color color = GetColorForValue(type.name);
            Color textColor = GetTextColorForValue(type.name);

            // Inicializar
            buttonItem.Setup(type.name, textColor, color);
        }

        StartCoroutine(AnimatePanels(mainPanel, detailsPanel));
    }

    public void BackToMain()
    {
        foreach (var btn in typesPanel.GetComponentsInChildren<Button>())
        {
            Destroy(btn.gameObject);
        }
        LayoutRebuilder.ForceRebuildLayoutImmediate(typesPanel as RectTransform);
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

    private Color GetColorForValue(string value)
    {
        switch (value)
        {
            case "Acero": return HexToColor("#60A2B9");
            case "Agua": return HexToColor("#2481EF");
            case "Bicho": return HexToColor("#92A212");
            case "Dragón": return HexToColor("#4F60E2");
            case "Eléctrico": return HexToColor("#FAC100");
            case "Fantasma": return HexToColor("#703F70");
            case "Fuego": return HexToColor("#E72324");
            case "Hada": return HexToColor("#EF70EF");
            case "Hielo": return HexToColor("#3DD9FF");
            case "Lucha": return HexToColor("#FF8100");
            case "Normal": return HexToColor("#A0A2A0");
            case "Planta": return HexToColor("#3DA224");
            case "Psíquico": return HexToColor("#EF3F7A");
            case "Roca": return HexToColor("#B0AA82");
            case "Siniestro": return HexToColor("#4F3F3D");
            case "Tierra": return HexToColor("#92501B");
            case "Veneno": return HexToColor("#923FCC");
            case "Volador": return HexToColor("#82BAEF");
            default: return Color.gray;
        }
    }
    
    private Color GetTextColorForValue(string value)
    {
        switch (value)
        {
            default: return Color.white;
        }
    }
    
    private Color HexToColor(string hex)
    {
        Color color;
        if (ColorUtility.TryParseHtmlString(hex, out color))
            return color;

        return Color.gray; // color de error
    }


}