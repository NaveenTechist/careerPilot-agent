"""
Modal Detector.

Detects and handles popups, cookie consent banners, privacy overlays,
and blocking modal dialogs before they intercept user clicks.

Handles modern SPA frameworks (Angular Material CDK, React portals, etc.)
where the backdrop/overlay and dialog content live in separate sibling
containers rather than parent-child relationships.
"""

import time
from playwright.sync_api import Page, Locator
from automation.utils.text_utils import TextUtils
from core.logger import app_logger


class ModalDetector:

    # -------------------------------------------------------
    # Selectors for modal containers
    # -------------------------------------------------------

    MODAL_SELECTORS = [
        "[role='dialog']:visible",
        "[role='alertdialog']:visible",
        "[aria-modal='true']:visible",
        # Angular Material CDK
        ".cdk-overlay-pane:visible",
        ".mat-dialog-container:visible",
        ".mat-mdc-dialog-container:visible",
        # Generic class patterns
        "div[class*='modal' i]:visible",
        "div[class*='popup' i]:visible",
        "div[class*='dialog' i]:visible",
        "div[class*='cookie' i]:visible",
        "div[class*='consent' i]:visible",
        "div[class*='privacy' i]:visible",
        "div[class*='banner' i]:visible",
        "[id*='cookie' i]:visible",
        "[id*='consent' i]:visible",
        "[class*='overlay' i]:visible",
        "[class*='backdrop' i]:visible",
    ]

    # -------------------------------------------------------
    # Keywords for consent / dismiss buttons
    # -------------------------------------------------------

    ACCEPT_KEYWORDS = [
        "i agree",
        "accept all",
        "accept",
        "agree",
        "allow",
        "ok",
        "got it",
        "consent",
        "proceed",
        "continue",
        "yes",
        "understand",
    ]

    DISMISS_KEYWORDS = [
        "close",
        "dismiss",
        "decline",
        "no thanks",
        "hide",
        "cancel",
    ]

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------

    @classmethod
    def detect_and_handle(cls, page: Page, application_id: str = None) -> str:
        """
        Scans for visible modals or cookie banners.
        Attempts to click the highest priority dismiss/accept button.
        Retries up to 3 times. Returns "WAITING_USER" if stuck, or "OK".
        """
        for attempt in range(3):
            modal = cls._find_active_modal(page)
            if not modal:
                return "OK"

            app_logger.info(
                f"Active modal/overlay detected (attempt {attempt + 1}/3). "
                "Scanning for dismiss button..."
            )

            # Try to find a dismiss button inside the modal element first,
            # then fall back to a full-page scan (handles Angular CDK / React
            # portals where backdrop and dialog are sibling containers).
            button = cls._find_modal_action_button(modal)
            if not button:
                app_logger.info(
                    "No button in modal container — scanning full page "
                    "for consent/agree buttons (CDK overlay fallback)."
                )
                button = cls._find_page_consent_button(page)

            if button:
                try:
                    btn_text = (
                        button.inner_text().strip()
                        or button.get_attribute("value")
                        or "Close"
                    )
                    app_logger.info(
                        f"Attempting to dismiss modal by clicking: '{btn_text}'"
                    )
                    button.scroll_into_view_if_needed(timeout=2000)
                    button.click(timeout=3000)
                    page.wait_for_timeout(1500)
                except Exception as e:
                    app_logger.warning(f"Normal click failed: {e}")
                    try:
                        button.click(force=True, timeout=2000)
                        page.wait_for_timeout(1500)
                    except Exception as force_err:
                        app_logger.error(f"Forced click also failed: {force_err}")
            else:
                app_logger.warning(
                    "Active modal detected, but no dismissal button found "
                    "in container or on page."
                )
                cls._log_modal_evidence(page, modal, application_id)
                page.wait_for_timeout(1500)

        # Final re-check
        if cls._find_active_modal(page):
            app_logger.warning(
                "Modal remains visible after 3 dismissal attempts."
            )
            return "WAITING_USER"

        return "OK"

    # -------------------------------------------------------
    # Modal detection
    # -------------------------------------------------------

    @classmethod
    def _find_active_modal(cls, page: Page) -> Locator | None:
        """
        Scans the page for visible modal elements with strict
        position / ARIA verification to avoid false positives
        on static layout elements.
        """
        for selector in cls.MODAL_SELECTORS:
            try:
                locator = page.locator(selector)
                count = locator.count()
                for i in range(count):
                    element = locator.nth(i)
                    if element.is_visible():
                        is_blocking = element.evaluate("""
                            (e) => {
                                const role = (e.getAttribute('role') || '').toLowerCase();
                                const ariaModal = (e.getAttribute('aria-modal') || '').toLowerCase();
                                if (role === 'dialog' || role === 'alertdialog' || ariaModal === 'true') {
                                    return true;
                                }

                                // Angular Material CDK overlay classes
                                const cls = (e.className || '').toString().toLowerCase();
                                if (cls.includes('cdk-overlay') || cls.includes('mat-dialog') || cls.includes('mat-mdc-dialog')) {
                                    return true;
                                }

                                const style = window.getComputedStyle(e);
                                const pos = style.position;
                                const isFixedOrAbsolute = pos === 'fixed' || pos === 'absolute';
                                const rect = e.getBoundingClientRect();

                                if (isFixedOrAbsolute && rect.width > 100 && rect.height > 50) {
                                    return true;
                                }
                                return false;
                            }
                        """)
                        if is_blocking:
                            return element
            except Exception:
                continue
        return None

    # -------------------------------------------------------
    # Button search — inside modal container
    # -------------------------------------------------------

    @classmethod
    def _find_modal_action_button(cls, modal: Locator) -> Locator | None:
        """
        Searches within a modal locator for consent or close buttons.
        """
        return cls._score_buttons(
            modal.locator(
                "button:visible, "
                "a:visible, "
                "input[type='submit']:visible, "
                "input[type='button']:visible, "
                "[role='button']:visible"
            )
        )

    # -------------------------------------------------------
    # Button search — full page fallback (CDK overlay / portals)
    # -------------------------------------------------------

    @classmethod
    def _find_page_consent_button(cls, page: Page) -> Locator | None:
        """
        Full-page scan for consent/agree buttons.
        Used as a fallback when Angular Material CDK, React portals,
        or other frameworks render the dialog content as a sibling
        to the backdrop instead of inside it.

        Only considers buttons whose text contains an ACCEPT keyword
        so we don't accidentally click unrelated page buttons.
        """
        return cls._score_buttons(
            page.locator(
                "button:visible, "
                "a:visible, "
                "input[type='submit']:visible, "
                "input[type='button']:visible, "
                "[role='button']:visible"
            ),
            require_accept=True,
        )

    # -------------------------------------------------------
    # Shared scoring logic
    # -------------------------------------------------------

    @classmethod
    def _score_buttons(
        cls,
        buttons: Locator,
        require_accept: bool = False,
    ) -> Locator | None:
        """
        Score candidate buttons by keyword match priority.
        Returns the best-scoring button above threshold, or None.
        """
        try:
            count = buttons.count()
            best_button = None
            best_score = -1

            for i in range(count):
                button = buttons.nth(i)
                try:
                    inner_text = button.inner_text() or ""
                    value = button.get_attribute("value") or ""
                    aria_label = button.get_attribute("aria-label") or ""
                    title = button.get_attribute("title") or ""

                    combined = " ".join([inner_text, value, aria_label, title])
                    text_norm = TextUtils.normalize(combined)
                except Exception:
                    continue

                if not text_norm:
                    continue

                score = 0

                # Accept actions — highest priority
                if any(kw in text_norm for kw in cls.ACCEPT_KEYWORDS):
                    score = 20
                    # Exact "i agree" or "accept all" gets extra weight
                    if "i agree" in text_norm or "accept all" in text_norm:
                        score = 25
                # Close / dismiss — secondary
                elif any(kw in text_norm for kw in cls.DISMISS_KEYWORDS):
                    if require_accept:
                        continue  # skip non-accept buttons in page-wide scan
                    score = 10
                # X close icon
                elif text_norm in ("x", "\u00d7"):
                    if require_accept:
                        continue
                    score = 15

                if score > best_score:
                    best_score = score
                    best_button = button

            if best_button and best_score > 0:
                return best_button
        except Exception as e:
            app_logger.error(f"Error scoring buttons: {e}")

        return None

    # -------------------------------------------------------
    # Evidence logging
    # -------------------------------------------------------

    @classmethod
    def _log_modal_evidence(
        cls,
        page: Page,
        modal: Locator,
        application_id: str | None,
    ):
        """
        Capture a screenshot and log the modal's HTML structure
        so developers can inspect exactly what overlay was blocking.
        """
        if not application_id:
            return

        # Screenshot
        try:
            from automation.services.screenshot_service import ScreenshotService
            ScreenshotService.save(
                page, application_id, "modal_no_dismiss_button.png"
            )
            app_logger.info(
                "Captured screenshot: modal_no_dismiss_button.png"
            )
        except Exception as e:
            app_logger.error(f"Failed to capture modal screenshot: {e}")

        # HTML structure
        try:
            from automation.services.automation_log_service import AutomationLogService
            html = modal.evaluate("e => e.outerHTML")
            truncated = html[:1500] + (
                "\n... [TRUNCATED] ..." if len(html) > 1500 else ""
            )
            AutomationLogService.log(
                application_id,
                f"[MODAL DETECTED] No dismissal button matched.\n"
                f"Modal HTML:\n{truncated}",
            )
        except Exception as e:
            app_logger.error(f"Failed to log modal HTML: {e}")
