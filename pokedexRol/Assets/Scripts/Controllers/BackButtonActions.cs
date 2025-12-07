using UnityEngine;
using UnityEngine.UI;

public class BackButtonActions : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        Button btn = this.GetComponent<Button>();
        btn.onClick.AddListener(() => UIManager.Instance.BackToMain());
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
