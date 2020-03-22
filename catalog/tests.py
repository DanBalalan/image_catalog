import os
from datetime import datetime

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .models import Image


class UploadTestCase(TestCase):
    client = Client()

    @classmethod
    def setUpTestData(cls):
        """
        Создание тестовых данных с различно заполненными полями
        для проверки корректности поиска, изменения атрибутов и удаления
        :return:
        """
        file_ = SimpleUploadedFile(name='go.jpg',
                                   content=open('catalog/tests/go.jpg', 'rb').read(),
                                   content_type='image/jpeg')
        cls.img1 = Image(
            file=file_,
            name='go',
            description=None,
            created=None,
        )
        cls.img2 = Image(
            file=file_,
            name='go',
            description='godescription',
            created=None,
        )
        cls.img3 = Image(
            file=file_,
            name='go',
            description='godescription',
            created=datetime(2007, 1, 1),
        )
        cls.img1.save()
        cls.img2.save()
        cls.img3.save()

    @classmethod
    def tearDownClass(cls):
        """
        Удаление созданных при тестах файлов записей
        :return:
        """
        cls.img1.delete()
        cls.img2.delete()
        cls.img3.delete()

    def test_upload_files(self):
        """
        Проверяет загрузку файла на сервер через /upload/ эндпоинт:
         - Корректное количество новых записей в бд
         - Наличие файлов изображений на локальном диске
        :return:
        """
        initial_images_count = Image.objects.count()
        initial_files = os.listdir(settings.MEDIA_ROOT)
        with open('catalog/tests/go.jpg', 'rb') as f:
            self.client.post(reverse('uploadimage'),
                             {'file': f, 'name': 'upload_test',
                              'description': 'upload_test',
                              'created': '2020-02-02'})
        images_count = Image.objects.count()
        assert initial_images_count + 1 == images_count
        files = os.listdir(settings.MEDIA_ROOT)
        difference = list(set(files) - set(initial_files))
        assert len(difference) == 1
        last_image = Image.objects.order_by('id').last()
        last_image.delete()

    def test_search(self):
        """
        Проверяет количество найденных изображений по разным критериям
        :return:
        """
        correct_answers = [3, 2, 1, 1, 0, 0]
        for i, el in enumerate((('go', '', ''),
                                ('', 'godescription', ''),
                                ('go', 'godescription', '2007-01-01'),
                                ('', '', '2007-01-01'),
                                ('', '', '2020-01-01'),
                                ('randomname', '', ''))):
            resp = self.client.post(reverse('imagesearch'),
                                    {'name': el[0], 'description': el[1], 'created': el[2]})
            count = resp.context[0]['images'].count()
            assert count == correct_answers[i]

    def test_alter_attribute(self):
        """
        Проверяет корректность изменения полей в бд у записи
        и ответ при некорректных данных (дата)
        :return:
        """
        new_attrs = {'name': 'newname',
                     'description': 'newdescription',
                     'created': '2020-02-02'}
        id_ = self.img1.id
        self.client.post(f'/detail/{id_}', {'name': new_attrs['name'],
                                            'description': new_attrs['description'],
                                            'created': new_attrs['created']})
        altered_img = Image.objects.get(pk=id_)
        assert altered_img.name == new_attrs['name']
        assert altered_img.description == new_attrs['description']
        assert altered_img.created == datetime.strptime(new_attrs['created'], '%Y-%m-%d').date()

        self.client.post(f'/detail/{id_}', {'created': '2020-55-55'})
        assert altered_img.created == datetime.strptime(new_attrs['created'], '%Y-%m-%d').date()

    def test_delete(self):
        """
        Проверяет удаление записи из бд и файла с диская
        :return:
        """
        id_ = self.img1.id
        file_ = self.img1.file.path
        initial_images_count = Image.objects.count()
        self.client.get(f'/delete/{id_}')
        images_count = Image.objects.count()
        assert initial_images_count - 1 == images_count
        assert not os.path.exists(os.path.join(settings.MEDIA_ROOT, file_))
