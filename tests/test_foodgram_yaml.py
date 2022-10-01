import os
import re

from .conftest import root_dir


class TestWorkflow:

    def test_workflow(self):
        foodgram_workflow_basename = 'foodgram_workflow'
        workflow_dir = os.path.join(
            root_dir, os.path.join('.github', 'workflows')
        )
        yaml = f'{foodgram_workflow_basename}.yaml'
        is_yaml = yaml in os.listdir(workflow_dir)

        yml = f'{foodgram_workflow_basename}.yml'
        is_yml = yml in os.listdir(workflow_dir)

        if not is_yaml and not is_yml:
            assert False, (
                f'В каталоге {workflow_dir} не найден файл '
                f'с описанием workflow {yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В каталоге {workflow_dir} не должно быть двух файлов '
                f'{foodgram_workflow_basename} с расширениями .yaml и .yml\n'
                'Удалите один из них!'
            )

        filename = yaml if is_yaml else yml

        try:
            with open(f'{os.path.join(workflow_dir, filename)}', 'r') as f:
                foodgram = f.read()
        except FileNotFoundError:
            assert False, (
                f'Проверьте, что добавили файл {filename} '
                f'в каталог {workflow_dir} для проверки'
            )

        assert (
            re.search(r'on:\s*push:\s*branches:\s*-\smaster', foodgram)
            or 'on: [push]' in foodgram
            or 'on: push' in foodgram
        ), f'Проверьте, что добавили действие при пуше в файл {filename}'
        assert 'pytest' in foodgram, (
            f'Проверьте, что добавили pytest в файл {filename}'
        )
        assert 'appleboy/ssh-action' in foodgram, (
            f'Проверьте, что добавили деплой в файл {filename}'
        )
        assert 'appleboy/telegram-action' in foodgram, (
            'Проверьте, что настроили отправку telegram сообщения '
            f'в файл {filename}'
        )
