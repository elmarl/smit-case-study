```bash
git clone https://github.com/elmarl/smit-case-study.git
cd smit-case-study
```

On windows:

```bash
python -m venv venv
venv\Scripts\activate
```

To install dependencies:

```bash
pip install -r requirements.txt
```

To start the application, run:

```bash
cd booking_app
uvicorn main:app --reload
```

To add/edit/delete providers, edit the file booking_app/providers_config.json

Right now it is as a config file, but can also be in DB with a simple admin panel for CRUD functionality.

I used the adapter pattern to enable communication with different API's, there is a adapter registry that registers these adapters on startup.
