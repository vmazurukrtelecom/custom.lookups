#!/usr/bin/python

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.vars.hostvars import HostVars
import json
from datetime import datetime

DOCUMENTATION = r'''
---
module: vars_dump
short_description: Dump all playbook variables to a file with a timestamp
description:
  - This lookup plugin writes all variables available in the current playbook context to a specified file,
    including a timestamp of when the dump was created.
  - The output is formatted as JSON for easy readability and parsing.
  - Handles non-JSON-serializable objects like HostVars by converting them to dictionaries.
options:
  file_path:
    description: The path to the file where variables will be written.
    default: "/tmp/variables.txt"
    type: str
author:
  - Your Name <your.email@example.com>
version_added: "1.0.0"
'''

EXAMPLES = r'''
- hosts: localhost
  tasks:
    - debug:
        msg: "{{ lookup('custom.lookups.vars_dump') }}"
    - debug:
        msg: "{{ lookup('custom.lookups.vars_dump', file_path='/tmp/custom_vars.txt') }}"
'''

RETURN = r'''
_raw:
  description: A list containing a single string confirming the variables were written to the file.
  type: list
  elements: str
'''

class LookupModule(LookupBase):
    def _convert_to_serializable(self, obj):
        """
        Convert non-JSON-serializable objects to a serializable format.

        Args:
            obj: The object to convert.

        Returns:
            A JSON-serializable representation of the object.
        """
        if isinstance(obj, HostVars):
            # Перетворюємо HostVars у словник
            return dict(obj)
        elif isinstance(obj, dict):
            # Рекурсивно обробляємо словники
            return {k: self._convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Рекурсивно обробляємо списки
            return [self._convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            # Базові типи вже серіалізовані
            return obj
        else:
            # Для інших типів повертаємо строкове представлення
            return str(obj)

    def run(self, terms, variables=None, **kwargs):
        """
        Write all playbook variables to a file with a timestamp.

        Args:
            terms (list): List of terms passed to the lookup (not used in this plugin).
            variables (dict, optional): Dictionary of all variables in the playbook context.
            **kwargs: Additional keyword arguments, including 'file_path'.

        Returns:
            list: A list with a single string message confirming the operation.

        Raises:
            AnsibleError: If variables are not provided or file writing fails.
        """
        # Перевіряємо наявність variables
        if variables is None:
            raise AnsibleError("No variables available in the current context")

        # Отримуємо шлях до файлу з kwargs або використовуємо значення за замовчуванням
        file_path = kwargs.get('file_path', '/tmp/variables.txt')

        # Генеруємо таймстамп
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Перетворюємо variables у серіалізований формат
        try:
            serializable_variables = self._convert_to_serializable(variables)
        except Exception as e:
            raise AnsibleError(f"Failed to convert variables to a serializable format: {str(e)}")

        # Формуємо дані для запису
        output_data = {
            "timestamp": timestamp,
            "variables": serializable_variables
        }

        # Записуємо у файл
        try:
            with open(file_path, 'w') as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            raise AnsibleError(f"Failed to write to {file_path}: {str(e)}")

        # Повертаємо результат як список
        return [f"Variables written to {file_path} with timestamp {timestamp}"]

# Тестування локально (опціонально)
if __name__ == "__main__":
    lookup = LookupModule()
    fake_vars = {"var1": "value1", "var2": 42}
    result = lookup.run([], variables=fake_vars, file_path="/tmp/test_vars.txt")
    print(result)
