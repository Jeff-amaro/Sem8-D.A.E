from rest_framework import viewsets
from rest_framework import filters
from .models import Exam, Question, Option
from .serializers import ExamSerializer, QuestionSerializer, OptionSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    filterset_fields = ['exam']
    ordering_fields = ['id']


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

