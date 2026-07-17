"""
Universal Robust Apply Detector.

Locates the primary "Apply" button or link on a job page
using advanced heuristics and a scoring system.
"""

from playwright.sync_api import Locator
from playwright.sync_api import Page

from automation.utils.text_utils import TextUtils
from core.logger import app_logger


class ApplyDetector:

    KEYWORDS = [
        "apply",
        "easy apply",
        "quick apply",
        "apply now",
        "start application",
        "continue application",
        "submit application",
        "submit resume",
        "apply for this job",
        "apply for this position",
        "apply on company site",
    ]

    IGNORE = [
        "save",
        "share",
        "login",
        "log in",
        "sign in",
        "register",
        "cancel",
        "close",
        "back",
    ]

    @classmethod
    def detect(
        cls,
        page: Page,
    ) -> Locator | None:
        """
        Scans candidate elements on the page, scores them using
        structural and visual heuristics, and returns the highest scoring locator.
        """
        try:
            # Query buttons, links, inputs, and common styled custom components
            selectors = (
                "button:visible, "
                "a:visible, "
                "input[type='submit']:visible, "
                "input[type='button']:visible, "
                "[role='button']:visible, "
                "div[class*='btn' i]:visible, "
                "div[class*='button' i]:visible, "
                "span[class*='btn' i]:visible, "
                "span[class*='button' i]:visible"
            )

            elements = page.locator(selectors)
            total = elements.count()

            best_element = None
            best_score = -999

            # Get page title and first visible heading as potential job titles
            heading_text = ""
            heading_y = -1
            try:
                first_heading = page.locator("h1:visible, h2:visible").first
                if first_heading.count() > 0:
                    heading_text = TextUtils.normalize(first_heading.inner_text())
                    box = first_heading.bounding_box()
                    if box:
                        heading_y = box["y"]
            except Exception:
                pass

            # Viewport heights for position calculation
            viewport = page.viewport_size or {"width": 1280, "height": 720}
            viewport_height = viewport["height"]

            for i in range(total):
                element = elements.nth(i)
                score = 0

                # 1. Text extraction and validation
                try:
                    inner_text = element.inner_text() or ""
                    value = element.get_attribute("value") or ""
                    aria_label = element.get_attribute("aria-label") or ""
                    title_attr = element.get_attribute("title") or ""
                    alt_attr = element.get_attribute("alt") or ""

                    combined_text = " ".join([inner_text, value, aria_label, title_attr, alt_attr])
                    text_norm = TextUtils.normalize(combined_text)
                except Exception:
                    continue

                if not text_norm:
                    continue

                # Filter out ignore patterns
                if any(word in text_norm for word in cls.IGNORE):
                    continue

                # Must match at least one apply keyword
                if not any(word in text_norm for word in cls.KEYWORDS):
                    continue

                # 2. Tag Weight Heuristics
                try:
                    tag = element.evaluate("e => e.tagName.toLowerCase()")
                    role = element.get_attribute("role") or ""
                    input_type = element.get_attribute("type") or ""
                except Exception:
                    tag = ""
                    role = ""
                    input_type = ""

                if tag in ["button", "input"] or role == "button" or input_type == "submit":
                    score += 10

                # 3. Text Priority Heuristics
                if any(word in text_norm for word in ["easy apply", "apply now", "start application", "continue application"]):
                    score += 15

                # 4. Position and Dimensions (Bounding Box) Heuristics
                try:
                    box = element.bounding_box()
                except Exception:
                    box = None

                if box:
                    x, y, w, h = box["x"], box["y"], box["width"], box["height"]

                    # Position Score
                    if y < 120:  # In navbar/header
                        score -= 20
                    elif 0.2 * viewport_height <= y <= 0.8 * viewport_height:  # Middle of the screen
                        score += 20

                    # Size Score
                    if w >= 100 and h >= 35:  # Large button
                        score += 15
                    elif w < 80 or h < 25:  # Chinna text link / tiny button
                        score += 0

                    # Proximity to main job heading
                    if heading_y != -1 and abs(y - heading_y) < 300:
                        score += 10
                else:
                    # Invisible or not rendered in layout
                    continue

                # 5. Color / CSS Class Heuristics
                try:
                    class_attr = element.get_attribute("class") or ""
                    class_norm = class_attr.lower()
                except Exception:
                    class_norm = ""

                if any(cls_name in class_norm for cls_name in ["primary", "btn-primary", "apply", "submit", "brand", "active"]):
                    score += 15

                # 6. Modal / Popup Detection
                # If the element has a modal/popup ancestor, prioritize it
                try:
                    is_in_modal = element.evaluate("""
                        (e) => {
                            let parent = e.parentElement;
                            while (parent) {
                                const cls = (parent.className || '').toString().toLowerCase();
                                const role = (parent.getAttribute('role') || '').toLowerCase();
                                if (cls.includes('modal') || cls.includes('dialog') || cls.includes('popup') || role === 'dialog') {
                                    return true;
                                }
                                parent = parent.parentElement;
                            }
                            return false;
                        }
                    """)
                except Exception:
                    is_in_modal = False

                if is_in_modal:
                    score += 50

                # Track the best scoring element
                if score > best_score:
                    best_score = score
                    best_element = element

            if best_element and best_score >= 0:
                app_logger.info(f"ApplyDetector found button with score {best_score}")
                return best_element

        except Exception as e:
            app_logger.error(f"Error in ApplyDetector: {e}")

        return None