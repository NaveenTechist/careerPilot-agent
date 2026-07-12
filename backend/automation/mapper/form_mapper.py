class FormMapper:

    @staticmethod
    def value(
        field_type,
        context,
    ):
        resume = context.resume
        profile = context.profile
        mapping = {
            "FIRST_NAME": resume.first_name,
            "LAST_NAME": resume.last_name,
            "EMAIL": resume.email,
            "PHONE": resume.phone,
            "LINKEDIN": resume.linkedin,
            "GITHUB": resume.github,
            "PORTFOLIO": resume.portfolio,
            "NOTICE_PERIOD": profile.notice_period,
            "CURRENT_CTC": profile.current_ctc,
            "EXPECTED_CTC": profile.expected_ctc,
        }

        return mapping.get(
            field_type.value,
        )