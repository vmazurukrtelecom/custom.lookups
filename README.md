# Custom Lookups Collection

Ця колекція містить lookup-плагін для Ansible `vars_dump`.

---
_created with support of grok3 (free tier))_


## Плагін `vars_dump`

Виводить змінні контексту плейбука 

---
основна причина / ідея розробки/тестування даного плагіну:


possibility of ansible AWX obtain credendials  **per machine** - via 3rd party lookup plugin


(i.e. ! NOT per template )


згідно статті https://www.redhat.com/en/blog/ansible-tower-feature-spotlight-custom-credentials

---
базово створено для тестування функціоналу передачі значнення inventory_host через inventory VARIABLES в custom_lookup_plugin 

(або по іншому - "динамічного" (per machine / host) використання ansible (!не AWX) lookup plugin функціоналу в "ніби статичних" inventory VARIABLES) 


але як пізніше виявлено -  значнення inventory_host можна і не передавати через параметри до custom_lookup_plugin;


 inventory_host можна отримати із variables котрі передаються в "стандатному виклику run" LookupModule
```
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
...

    inventory_hostname = variables.get('inventory_hostname')

```

`variables (dict, optional): Dictionary of all variables in the playbook context.`



окрема замітка:

lookup_plugin найпростіше встановлювати через collections;

відповідно додано collections/requirements.yml


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

