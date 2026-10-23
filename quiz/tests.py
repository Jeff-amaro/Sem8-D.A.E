from rest_framework import status
from rest_framework.test import APITestCase
from .models import Exam, Question


class ExamAPITests(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(
            title='Python Basics',
            description='Intro',
        )

    def test_list_exams(self):
        response = self.client.get('/api/exams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_exam(self):
        response = self.client.post(
            '/api/exams/',
            {'title': 'New Exam', 'description': 'Created in test'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_required_field(self):
        response = self.client.post(
            '/api/exams/',
            {'description': 'No title'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_wrong_type(self):
        response = self.client.post(
            '/api/exams/',
            {'title': 'Valid', 'description': 12345},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionAPITests(APITestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title='Math', description='Basic math')

    def test_create_question_with_one_correct_option(self):
        payload = {
            'text': 'What is 2 + 2?',
            'exam': self.exam.id,
            'options': [
                {'text': '4', 'is_correct': True},
                {'text': '5', 'is_correct': False},
            ],
        }
        response = self.client.post('/api/questions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['options'][0]['text'], '4')

    def test_two_correct_options_are_rejected(self):
        payload = {
            'text': 'Pick one',
            'exam': self.exam.id,
            'options': [
                {'text': 'A', 'is_correct': True},
                {'text': 'B', 'is_correct': True},
            ],
        }
        response = self.client.post('/api/questions/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_without_options_is_rejected(self):
        response = self.client.post(
            '/api/questions/',
            {'text': 'No options', 'exam': self.exam.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_questions_by_exam(self):
        other_exam = Exam.objects.create(title='Science', description='Other')
        Question.objects.create(text='Math question', exam=self.exam)
        Question.objects.create(text='Science question', exam=other_exam)
        response = self.client.get(f'/api/questions/?exam={self.exam.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_questions_by_text(self):
        Question.objects.create(text='Django REST framework', exam=self.exam)
        Question.objects.create(text='Something else', exam=self.exam)
        response = self.client.get('/api/questions/?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_wrong_exam_type_is_rejected(self):
        response = self.client.post(
            '/api/questions/',
            {'text': 'Bad exam', 'exam': 'not-an-id'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
