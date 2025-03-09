#!/usr/bin/python

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.vars.hostvars import HostVars, HostVarsVars
import json
from datetime import datetime

DOCUMENTATION = r'''
---
module: vars_dump
short_description: Return all playbook variables as a JSON string with a timestamp
description:
  - This lookup plugin returns all variables available in the current playbook context as a JSON-formatted string,
    including a timestamp of when the dump was created.
  - Useful for debugging or logging variables directly in playbook output.
author:
  - Your Name <your.email@example.com>
version_added: "1.0.0"
'''

EXAMPLES = r'''
- hosts: localhost
  tasks:
    - debug:
        msg: "{{ lookup('custom.lookups.vars_dump') }}"
'''

RETURN = r'''
_raw:
  description: A list containing a single JSON-formatted string with the timestamp and all playbook variables.
  type: list
  elements: str
'''

class LookupModule(LookupBase):
    def _convert_to_serializable(self, obj, depth=0, max_depth=10):
        """
        Convert non-JSON-serializable objects to a serializable format.

        Args:
            obj: The object to convert.
            depth: Current recursion depth to prevent infinite loops.
            max_depth: Maximum recursion depth to avoid stack overflow.

        Returns:
            A JSON-serializable representation of the object.
        """
        if depth > max_depth:
            return f"Max recursion depth ({max_depth}) exceeded: {str(obj)}"

        if isinstance(obj, (HostVars, HostVarsVars)):
            # Перетворюємо HostVars або HostVarsVars у словник
            try:
                return {k: self._convert_to_serializable(v, depth + 1, max_depth) for k, v in obj.items()}
            except AttributeError:
                return str(obj)
        elif isinstance(obj, dict):
            # Рекурсивно обробляємо словники
            return {k: self._convert_to_serializable(v, depth + 1, max_depth) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Рекурсивно обробляємо списки
            return [self._convert_to_serializable(item, depth + 1, max_depth) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            # Базові типи вже серіалізовані
            return obj
        else:
            # Універсальна обробка: спробуємо отримати словник або повернемо рядок
            try:
                return {k: self._convert_to_serializable(v, depth + 1, max_depth) for k, v in obj.items()}
            except (TypeError, AttributeError, ValueError):
                return str(obj)

    def run(self, terms, variables=None, **kwargs):
        """
        Return all playbook variables as a JSON string with a timestamp.

        Args:
            terms (list): List of terms passed to the lookup (not used in this plugin).
            variables (dict, optional): Dictionary of all variables in the playbook context.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list with a single JSON-formatted string containing the timestamp and variables.

        Raises:
            AnsibleError: If variables are not provided or serialization fails.
        """
        # Перевіряємо наявність variables
        if variables is None:
            raise AnsibleError("No variables available in the current context")

        # Генеруємо таймстамп
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Перетворюємо variables у серіалізований формат
        try:
            serializable_variables = self._convert_to_serializable(variables)
        except Exception as e:
            raise AnsibleError(f"Failed to convert variables to a serializable format: {str(e)}")

        # Формуємо дані
        output_data = {
            "timestamp": timestamp,
            "variables": serializable_variables
        }

        # Перетворюємо дані в JSON-рядок
        try:
            json_output = json.dumps(output_data, indent=4, ensure_ascii=False)
        except Exception as e:
            raise AnsibleError(f"Failed to serialize data to JSON: {str(e)}")

        # Повертаємо результат як список із одним JSON-рядком
        return [json_output]

# Тестування локально (опціонально)
if __name__ == "__main__":
    lookup = LookupModule()
    fake_vars = {"var1": "value1", "var2": 42}
    result = lookup.run([], variables=fake_vars)
    print(result[0])
