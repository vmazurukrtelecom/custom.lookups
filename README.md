# Custom Lookups Collection

Ця колекція містить lookup-плагіни для Ansible. Наразі доступний плагін `vars_dump`.

## Плагін `vars_dump`

Записує всі змінні контексту плейбука у файл із таймстампом.

### Використання
```yaml
- hosts: localhost
  tasks:
    - debug:
        msg: "{{ lookup('custom.lookups.vars_dump', file_path='/path/to/custom_file.txt') }}"

