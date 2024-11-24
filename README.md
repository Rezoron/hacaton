git clone https://github.com/Rezoron/hacaton.git

cd hacaton

git checkout view

pip install -r req.txt


### Запуск

Запустить эти 2 команды в разных консолях.

```
uvicorn view.main:app --host 127.0.0.1 --port 8080 --reload

uvicorn upload_service.main:app --host 127.0.0.1 --port 8000 --reload
```