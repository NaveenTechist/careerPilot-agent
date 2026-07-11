from automation.detector.form_detector import FormDetector

from automation.classifier.field_classifier import FieldClassifier

from automation.mapper.form_mapper import FormMapper

from automation.engine.fill_engine import FillEngine


class FormEngine:

    @staticmethod
    def process(

        page,

        context,

    ):

        fields = FormDetector.scan(page)

        for field in fields:

            field_type = FieldClassifier.classify(

                field

            )

            value = FormMapper.value(

                field_type,

                context,

            )

            FillEngine.fill(

                page,

                field,

                value,

            )