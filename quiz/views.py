from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from .models import Exam, Question, Option
from .serializers import ExamSerializer, QuestionSerializer, OptionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'created_at']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['exam']
    search_fields = ['text']
    ordering_fields = ['id', 'created_at']


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filterset_fields = ['question', 'is_correct']
