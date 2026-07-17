from automation.detector.form_detector import FormDetector
from automation.classifier.field_classifier import FieldClassifier
from automation.mapper.form_mapper import FormMapper
from automation.filler.field_filler import FieldFiller
from automation.parser.field_parser import FieldParser
from automation.matcher.answer_matcher import AnswerMatcher


class FormEngine:
    @staticmethod
    def process(
        page,
        resume,
    ):
        fields = FieldParser.parse(page)
        for field in fields:
            answer = AnswerMatcher.match(
                field=field,
                resume=resume,
            )
            if answer is None:
                continue
            FieldFiller.fill(
                field,
                answer,
            )