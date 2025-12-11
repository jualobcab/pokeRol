using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class TypeButton : MonoBehaviour
{
    public TMP_Text label;
    public Image background;

    public void Setup(string texto, Color textColor, Sprite sprite)
    {
        label.text = texto;
        label.color = textColor;
        background.sprite = sprite;
    }
}
