from playwright.sync_api import Locator


class LabelParser:

    @staticmethod
    def parse(locator: Locator) -> str:
        try:
            label = locator.evaluate("""
(element) => {
    // --- Step 1: Get the option's own label text ---
    let optionText = "";
    if (element.labels && element.labels.length) {
        optionText = element.labels[0].innerText;
    } else if (element.id) {
        const lbl = document.querySelector(`label[for="${element.id}"]`);
        if (lbl) optionText = lbl.innerText;
    }
    if (!optionText) {
        const parentLabel = element.closest("label");
        if (parentLabel) optionText = parentLabel.innerText;
    }
    optionText = (optionText || "").trim();

    // --- Step 2: For radio/checkbox, find the group question heading ---
    const type = (element.getAttribute("type") || "").toLowerCase();
    if (type !== "radio" && type !== "checkbox") {
        return optionText;
    }

    // Find the common ancestor container that holds ALL options
    // in this radio/checkbox group, then look for a heading inside it
    // that does NOT contain any <input> descendants (pure text heading).
    const name = element.getAttribute("name");

    // Strategy A: Use the name attribute to find sibling inputs and
    // derive their lowest common ancestor (the group container).
    let groupContainer = null;
    if (name) {
        const siblings = document.querySelectorAll(
            `input[name="${CSS.escape(name)}"]`
        );
        if (siblings.length > 1) {
            // Walk up from the first sibling until we find an ancestor
            // that contains ALL siblings.
            let candidate = siblings[0].parentElement;
            for (let d = 0; d < 10 && candidate; d++) {
                let containsAll = true;
                for (const sib of siblings) {
                    if (!candidate.contains(sib)) {
                        containsAll = false;
                        break;
                    }
                }
                if (containsAll) {
                    groupContainer = candidate;
                    break;
                }
                candidate = candidate.parentElement;
            }
        }
    }

    // Strategy B: If no name or single input, walk up manually.
    if (!groupContainer) {
        groupContainer = element.parentElement;
        for (let d = 0; d < 6 && groupContainer; d++) {
            // Stop at fieldset or any container with multiple inputs
            const inputs = groupContainer.querySelectorAll(
                "input[type='radio'], input[type='checkbox']"
            );
            if (inputs.length > 1) break;
            groupContainer = groupContainer.parentElement;
        }
    }

    if (!groupContainer) return optionText;

    // --- Step 3: Search for a question heading INSIDE the group container ---
    // A valid heading must:
    //   - NOT contain any <input> descendants (otherwise it's an option wrapper)
    //   - Have meaningful text
    //   - Not be the same text as one of the options
    const headingSelectors = [
        "legend",
        "[class*='question' i]",
        "[class*='title' i]",
        "[class*='header' i]",
        "h1", "h2", "h3", "h4", "h5", "h6",
    ];

    let questionText = "";
    for (const sel of headingSelectors) {
        const candidates = groupContainer.querySelectorAll(sel);
        for (const c of candidates) {
            // Must not contain any radio/checkbox inputs
            if (c.querySelector("input[type='radio'], input[type='checkbox']")) {
                continue;
            }
            const text = (c.innerText || "").trim();
            if (text && text.length > 1) {
                questionText = text;
                break;
            }
        }
        if (questionText) break;
    }

    // Fallback: check for a [class*='label'] that is NOT a <label> tag
    // and does NOT wrap an <input>.
    if (!questionText) {
        const labelCandidates = groupContainer.querySelectorAll(
            "[class*='label' i]"
        );
        for (const c of labelCandidates) {
            if (c.tagName === "LABEL") continue;
            if (c.querySelector("input")) continue;
            const text = (c.innerText || "").trim();
            if (text && text.length > 1) {
                questionText = text;
                break;
            }
        }
    }

    if (questionText) {
        // Strip trailing asterisks and whitespace
        questionText = questionText.replace(/[\\s*]+$/g, "").trim();
        return questionText + " -> " + optionText;
    }

    return optionText;
}
""")
            return label.strip()
        except Exception:
            return ""