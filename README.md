# Project Configuration

## Environment Setup

To run this project, a `.env` file must be created in the root directory of the repository. This file should contain the following starting configuration:

```plaintext
APP_ENV=local
```

The `APP_ENV` variable determines the environment in which the application will run. Possible values are:
- `local`
- `development`
- `production`

## Environment-Specific Configuration

In addition to the `.env` file, you need to create specific configuration files for the `development` and `production` environments.

**NOTE:** Those configurations are needed to start the project, if those files are not present and populated the project won't start

### Development Configuration

Create a file named `development.py` inside the `configurations` directory with the following content:

```python
from configurations.base import BaseConfig

class DevelopmentConfig(BaseConfig):
    <VAR_NAME> : <TYPE> = <VALUE>
    ...
```

### Production Configuration

Create a file named `production.py` inside the `configurations` directory with the following content:

```python
from configurations.base import BaseConfig

class ProductionConfig(BaseConfig):
    <VAR_NAME> : <TYPE> = <VALUE>
    ...
```

### Adding Environment Variables

Each configuration file can include additional environment-specific variables as needed. For example, you can add API keys, secret keys, or any other settings specific to the environment.