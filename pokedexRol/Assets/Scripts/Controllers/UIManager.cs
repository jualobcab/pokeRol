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
    public Sprite[] typeBadges;

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
            //Color color = GetColorForValue(type.name);
            Color textColor = GetTextColorForValue(type.name);

            // Inicializar
            buttonItem.Setup(type.name, textColor, GetSpriteForValue(type.name));
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

    private Sprite GetSpriteForValue(string value)
    {
        switch (value)
        {
            case "Acero": return typeBadges[0];
            case "Agua": return typeBadges[1];
            case "Bicho": return typeBadges[2];
            case "Dragón": return typeBadges[3];
            case "Eléctrico": return typeBadges[4];
            case "Fantasma": return typeBadges[5];
            case "Fuego": return typeBadges[6];
            case "Hada": return typeBadges[7];
            case "Hielo": return typeBadges[8];
            case "Lucha": return typeBadges[9];
            case "Normal": return typeBadges[10];
            case "Planta": return typeBadges[11];
            case "Psíquico": return typeBadges[12];
            case "Roca": return typeBadges[13];
            case "Siniestro": return typeBadges[14];
            case "Tierra": return typeBadges[15];
            case "Veneno": return typeBadges[16];
            case "Volador": return typeBadges[17];
            default: return typeBadges[10];
        }
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
            default: return HexToColor("#FFFFFF00");
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