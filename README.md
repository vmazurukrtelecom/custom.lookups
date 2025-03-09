# Custom Lookups Collection

Ця колекція містить lookup-плагіни для Ansible. Наразі доступний плагін `vars_dump`.

## Плагін `vars_dump`

Виводить змінні контексту плейбука 

створено для тестування функціоналу inventory VARIABLES

згідно статті https://www.redhat.com/en/blog/ansible-tower-feature-spotlight-custom-credentials


created with support of grok3 (free tier))


### Використання lookup (в playbook)
```yaml
- hosts: all
  tasks:
    - name: Dump inventory_hostname to msg
      debug:
        msg: "{{ lookup('custom.lookups.vars_dump') }}"
```


### Використання lookup (в inventory VARIABLES)

приклад 

```
---
test_variable1: "{{ lookup('custom.lookups.vars_dump') }}"
```
![image](https://github.com/user-attachments/assets/489cf672-9520-4ac9-a60b-70121af10e75)

![image](https://github.com/user-attachments/assets/cac68dcf-51b1-4993-ac9d-89cc5e7b5bbf)

![image](https://github.com/user-attachments/assets/42c99c9c-f040-4947-9ce5-7bcb4c91f9eb)

RES:

![image](https://github.com/user-attachments/assets/94a7f5f1-a47f-4627-b376-7ca9110910f6)

