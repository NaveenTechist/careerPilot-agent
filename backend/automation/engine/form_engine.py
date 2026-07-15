from automation.detector.form_detector import FormDetector
from automation.classifier.field_classifier import FieldClassifier
from automation.mapper.form_mapper import FormMapper
from automation.filler.field_filler import FieldFiller
from automation.parser.field_parser import FieldParser


class FormEngine:

    @staticmethod
    def process(
        page,
        context,
    ):

        fields = FieldParser.parse(page)
        for field in fields:
            print(
                field.label,
                field.field_type,
            )

            value = FormMapper.value(
                field_type,
                context,
            )

            FieldFiller.fill(
                page,
                field,
                value,
            )