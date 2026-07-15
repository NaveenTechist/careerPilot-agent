from playwright.sync_api import Locator


class LabelParser:

    @staticmethod
    def parse(locator: Locator) -> str:
        try:
            label = locator.evaluate("""
(element) => {
    if(element.labels && element.labels.length){
        return element.labels[0].innerText;
    }
    if(element.id){
        const lbl=document.querySelector(
            `label[for="${element.id}"]`
        );
        if(lbl) return lbl.innerText;
    }
    const parent=element.closest("label");
    if(parent) return parent.innerText;
    return "";
}
""")
            return label.strip()
        except Exception:
            return ""