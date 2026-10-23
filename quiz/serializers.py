from rest_framework import serializers
from .models import Exam, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'question']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'exam', 'options']
        read_only_fields = ['id']

    def validate(self, attrs):
        # When creating/updating via nested data is not enforced here;
        # validation focuses on ensuring exactly one correct option
        # by inspecting options passed in context or after creation is limited.
        # Enforce: when options are provided in initial data for create/update,
        # require exactly one with is_correct True
        options_data = self.initial_data.get('options') if hasattr(self, 'initial_data') else None
        if isinstance(options_data, list):
            correct_count = 0
            for opt in options_data:
                if isinstance(opt, dict) and opt.get('is_correct'):
                    correct_count += 1
            if correct_count != 1:
                raise serializers.ValidationError('A question must have exactly one correct option.')
        return attrs


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at', 'questions']
        read_only_fields = ['id', 'created_at']
