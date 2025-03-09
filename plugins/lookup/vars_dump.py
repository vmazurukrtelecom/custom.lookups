#!/usr/bin/python

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import json
from datetime import datetime

DOCUMENTATION = r'''
---
module: vars_dump
short_description: Return the inventory_hostname as a JSON string with a timestamp
description:
  - This lookup plugin returns the inventory_hostname variable from the current playbook context as a JSON-formatted string,
    including a timestamp of when the dump was created.
  - Useful for debugging or logging the inventory_hostname directly in playbook output.
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
  description: A list containing a single JSON-formatted string with the timestamp and inventory_hostname.
  type: list
  elements: str
'''

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        """
        Return the inventory_hostname as a JSON string with a timestamp.

        Args:
            terms (list): List of terms passed to the lookup (not used in this plugin).
            variables (dict, optional): Dictionary of all variables in the playbook context.
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list with a single JSON-formatted string containing the timestamp and inventory_hostname.

        Raises:
            AnsibleError: If variables are not provided or inventory_hostname is missing.
        """
        # Перевіряємо наявність variables
        if variables is None:
            raise AnsibleError("No variables available in the current context")

        # Отримуємо inventory_hostname
        inventory_hostname = variables.get('inventory_hostname')
        if inventory_hostname is None:
            raise AnsibleError("inventory_hostname is not available in the current context")

        # Генеруємо таймстамп
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Формуємо дані
        output_data = {
            "timestamp": timestamp,
            "inventory_hostname": inventory_hostname
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
    fake_vars = {"inventory_hostname": "test_host"}
    result = lookup.run([], variables=fake_vars)
    print(result[0])
