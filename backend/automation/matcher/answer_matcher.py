"""
Answer Matcher.

Maps detected form fields
to resume/application values.
"""

from automation.models.field import Field
from automation.models.field_type import FieldType


class AnswerMatcher:

    @staticmethod
    def _get_education(resume_json):
        edu_list = resume_json.get("education", [])
        if edu_list and isinstance(edu_list, list):
            return edu_list[0]
        return {}

    @staticmethod
    def _normalize_grade_to_10(grade_str):
        if not grade_str:
            return None
        import re
        nums = re.findall(r"\d+\.\d+|\d+", grade_str)
        if not nums:
            return None
        try:
            val = float(nums[0])
            if len(nums) > 1:
                scale = float(nums[1])
                if scale > 0:
                    return (val / scale) * 10.0
            if val <= 4.0:
                return (val / 4.0) * 10.0
            if val <= 10.0:
                return val
            if val <= 100.0:
                return (val / 100.0) * 10.0
        except Exception:
            pass
        return None

    @staticmethod
    def _parse_range(text):
        import re
        nums = re.findall(r"\d+\.\d+|\d+", text)
        if len(nums) == 2:
            try:
                return float(nums[0]), float(nums[1])
            except ValueError:
                pass
        return None

    @classmethod
    def match(
        cls,
        field,
        resume_json,
        resume_path,
    ):
        if not resume_json:
            resume_json = {}

        label = (
            field.label
            or field.placeholder
            or field.name
        ).lower()

        # 1. Handle File Uploads (Resume)
        if field.field_type == FieldType.FILE:
            return resume_path

        # 2. Extract context for Radio options ("Question -> Option")
        is_radio_option = "->" in field.label
        q_text = label.split("->")[0].strip() if is_radio_option else label
        opt_text = label.split("->")[-1].strip() if is_radio_option else ""

        # -----------------------------
        # Contact & Personal Information
        # -----------------------------
        if "first" in q_text and "name" in q_text:
            val = resume_json.get("first_name")
            if not val and resume_json.get("name"):
                val = resume_json.get("name").split()[0]
            return val

        if "last" in q_text and "name" in q_text:
            val = resume_json.get("last_name")
            if not val and resume_json.get("name"):
                parts = resume_json.get("name").split()
                if len(parts) > 1:
                    val = " ".join(parts[1:])
                else:
                    val = "N/A"
            return val

        if q_text == "name" or q_text == "full name":
            return resume_json.get("name")

        if "email" in q_text:
            return resume_json.get("email")

        # Check for separate country code/calling code field first
        if any(w in q_text for w in ["country code", "calling code", "dial code", "phone code", "dialing code"]):
            return "+91"

        if "phone" in q_text or "mobile" in q_text or "telephone" in q_text or q_text.startswith("tel") or " tel " in q_text or " tel:" in q_text or " tel." in q_text:
            val = resume_json.get("phone")
            if val:
                # Clean phone number (digits only for length checking)
                digits = "".join(c for c in str(val) if c.isdigit())
                # If there's a separate country code field, we should strip country code from main phone input.
                # E.g. Indian 12-digit number starting with 91 -> return last 10 digits.
                if len(digits) == 12 and digits.startswith("91"):
                    return digits[2:]
                # US 11-digit number starting with 1 -> return last 10 digits.
                if len(digits) == 11 and digits.startswith("1"):
                    return digits[1:]
                
                # Keep original cleaned formatting if not standard 12/11 digit country code prefix
                cleaned = "".join(c for c in str(val) if c.isdigit() or c in ("-", "(", ")"))
                return cleaned
            return None

        # -----------------------------
        # Location
        # -----------------------------
        if "city" in q_text:
            val = resume_json.get("city")
            if not val and resume_json.get("location"):
                val = resume_json.get("location").split(",")[0].strip()
            return val

        if "country" in q_text:
            val = resume_json.get("country")
            if not val and resume_json.get("location"):
                parts = resume_json.get("location").split(",")
                if len(parts) > 1:
                    val = parts[-1].strip()
                else:
                    val = "India"  # standard fallback
            return val

        if "state" in q_text or "province" in q_text:
            return resume_json.get("state") or "Karnataka"

        # -----------------------------
        # Links
        # -----------------------------
        if "linkedin" in q_text:
            return resume_json.get("linkedin")
        if "github" in q_text:
            return resume_json.get("github")
        if "portfolio" in q_text or "website" in q_text:
            return resume_json.get("portfolio") or resume_json.get("github")

        # -----------------------------
        # Education details
        # -----------------------------
        edu = cls._get_education(resume_json)

        # College / Institution Name
        if "college" in q_text or "university" in q_text or "institution" in q_text or "school" in q_text:
            if "city" in q_text or "location" in q_text:
                return resume_json.get("city") or "Vijayawada"
            return edu.get("institution")

        # Degree (B.Tech, B.E, Master, etc.)
        if "degree" in q_text or "qualification" in q_text:
            deg = edu.get("degree", "").lower()
            if not deg:
                deg = "b.tech"
            if is_radio_option:
                if any(w in opt_text for w in ["b.e", "b.tech", "btech", "bachelor"]):
                    return any(w in deg for w in ["b.e", "b.tech", "btech", "bachelor", "degree", "undergrad"])
                if any(w in opt_text for w in ["master", "m.s", "m.tech", "mtech"]):
                    return any(w in deg for w in ["master", "m.s", "m.tech", "mtech", "postgrad"])
                return "other" in opt_text
            return edu.get("degree")

        # Branch / Specialization / Major
        if "branch" in q_text or "speciali" in q_text or "major" in q_text or "field of study" in q_text:
            spec = (edu.get("specialization") or edu.get("degree") or "").lower()
            if not spec:
                spec = "information technology"
            if is_radio_option:
                if "computer" in opt_text or "cs" in opt_text:
                    return any(w in spec for w in ["computer", "cs", "it", "information"])
                if "information" in opt_text or "it" in opt_text:
                    return any(w in spec for w in ["information", "it"])
                if "electronics" in opt_text or "ece" in opt_text or "communication" in opt_text:
                    return any(w in spec for w in ["electronics", "ece", "telecommunication", "communication"])
                if "electrical" in opt_text or "ee" in opt_text:
                    return any(w in spec for w in ["electrical", "ee"])
                if "mechanical" in opt_text or "mech" in opt_text:
                    return any(w in spec for w in ["mechanical", "mech"])
                if "civil" in opt_text:
                    return "civil" in spec
                return "other" in opt_text
            return edu.get("specialization") or "Information Technology"

        # Year of Graduation
        if "graduation" in q_text or "year of grad" in q_text or "completion year" in q_text:
            grad_year = "2026"  # standard fallback for class of 2026
            if is_radio_option:
                return grad_year in opt_text
            return grad_year

        # CGPA Exact
        if "exact cgpa" in q_text or "exact gpa" in q_text or (q_text == "cgpa" or q_text == "gpa"):
            grade = edu.get("grade")
            if grade:
                import re
                nums = re.findall(r"\d+\.\d+|\d+", str(grade))
                if nums:
                    return nums[0]
            return "7.2"

        # CGPA Range (e.g. "7.00 to 7.99")
        if "range" in q_text and ("cgpa" in q_text or "gpa" in q_text or "grade" in q_text):
            if is_radio_option:
                grade_val = cls._normalize_grade_to_10(edu.get("grade") or "7.2")
                if grade_val is not None:
                    r = cls._parse_range(opt_text)
                    if r:
                        return r[0] <= grade_val <= r[1]
                    if "below" in opt_text:
                        import re
                        nums = re.findall(r"\d+\.\d+|\d+", opt_text)
                        if nums:
                            return grade_val < float(nums[0])
                    if "above" in opt_text:
                        import re
                        nums = re.findall(r"\d+\.\d+|\d+", opt_text)
                        if nums:
                            return grade_val > float(nums[0])
                return False

        # -----------------------------
        # Yes/No Questionnaires (demographic, backlogs, employment)
        # -----------------------------
        if is_radio_option:
            # Active backlogs: "Do you currently have any active backlogs..."
            if "backlog" in q_text:
                return opt_text == "no"

            # Available immediately / 6-months internship
            if "intern" in q_text or "available" in q_text:
                return opt_text == "yes"

            # Currently employed / holding other offers
            if "employed" in q_text or "holding an offer" in q_text or "other company" in q_text:
                return opt_text == "no"

            # Appeared for recruitment process in last 12 months
            if "recruitment process" in q_text or "appeared" in q_text or "last 12 months" in q_text:
                return opt_text == "no"

            # Gender
            if "gender" in q_text:
                return "male" in opt_text

            # Veteran
            if "veteran" in q_text or "military" in q_text:
                return "no" in opt_text or "decline" in opt_text

            # Disability
            if "disability" in q_text or "disabled" in q_text:
                return "no" in opt_text or "decline" in opt_text

        # -----------------------------
        # Consent & Settings Checkboxes
        # -----------------------------
        if field.field_type == FieldType.CHECKBOX:
            if any(w in q_text for w in ["save", "agree", "consent", "term", "policy", "receive"]):
                return True

        return None