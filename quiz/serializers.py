from rest_framework import serializers
from .models import Exam, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct', 'question']
        read_only_fields = ['id', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'exam', 'options']
        read_only_fields = ['id']

    def validate(self, attrs):
        error = 'A question must have exactly one correct option.'
        options = attrs.get('options')
        if options is None:
            if self.instance is None:
                raise serializers.ValidationError({'options': error})
            options = list(self.instance.options.all())
        correct_count = 0
        for option in options:
            if isinstance(option, dict):
                is_correct = option.get('is_correct', False)
            else:
                is_correct = option.is_correct
            if is_correct:
                correct_count += 1
        if correct_count != 1:
            raise serializers.ValidationError({'options': error})
        return attrs

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        Option.objects.bulk_create(
            [Option(question=question, **option) for option in options_data]
        )
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        instance = super().update(instance, validated_data)
        if options_data is not None:
            instance.options.all().delete()
            new_options = [
                Option(question=instance, **option)
                for option in options_data
            ]
            Option.objects.bulk_create(new_options)
        return instance


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'created_at', 'questions']
        read_only_fields = ['id', 'created_at']
