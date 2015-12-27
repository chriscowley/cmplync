# Cmplync

Needs an environment file for the settings called `.envs`

```
export SQLALCHEMY_DATABASE_URI="sqlite:////tmp/complyns.db"
```

Also `config.py`:

```
import os
SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = "SOME SECRET"
```
