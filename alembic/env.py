# # import os
# # import sys
# # from logging.config import fileConfig

# # from sqlalchemy import engine_from_config, pool

# # from alembic import context

# # import sys
# # from pathlib import Path

# # # Add this at the top (after the imports)
# # sys.path.append(str(Path(__file__).parent.parent))

# # # Then find where it sets target_metadata and change it to:
# # from src.git_day_practice.db import Base
# # target_metadata = Base.metadata

# # # Add the parent directory to path so we can import our modules
# # sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# # # Import our models and settings
# # from src.git_day_practice.models import Base
# # from src.git_day_practice.settings import get_settings

# # # this is the Alembic Config object
# # config = context.config

# # # Interpret the config file for Python logging
# # if config.config_file_name is not None:
# #     fileConfig(config.config_file_name)

# # # Set target metadata for autogenerate
# # target_metadata = Base.metadata


# # def run_migrations_offline() -> None:
# #     """Run migrations in 'offline' mode."""
# #     url = config.get_main_option("sqlalchemy.url")
# #     context.configure(
# #         url=url,
# #         target_metadata=target_metadata,
# #         literal_binds=True,
# #         dialect_opts={"paramstyle": "named"},
# #     )

# #     with context.begin_transaction():
# #         context.run_migrations()


# # def run_migrations_online() -> None:
# #     """Run migrations in 'online' mode."""
# #     # Get settings and set database URL
# #     settings = get_settings()
# #     configuration = config.get_section(config.config_ini_section)
# #     configuration["sqlalchemy.url"] = settings.database_url

# #     connectable = engine_from_config(
# #         configuration,
# #         prefix="sqlalchemy.",
# #         poolclass=pool.NullPool,
# #     )

# #     with connectable.connect() as connection:
# #         context.configure(connection=connection, target_metadata=target_metadata)

# #         with context.begin_transaction():
# #             context.run_migrations()


# # if context.is_offline_mode():
# #     run_migrations_offline()
# # else:
# #     run_migrations_online()


# import sys
# from pathlib import Path
# from logging.config import fileConfig

# from sqlalchemy import engine_from_config
# from sqlalchemy import pool

# from alembic import context

# # Add the project root to Python path
# sys.path.append(str(Path(__file__).parent.parent))

# # Import your models
# from src.git_day_practice.db import Base
# from src.git_day_practice import models

# # this is the Alembic Config object
# config = context.config

# # Interpret the config file for Python logging.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Set the target metadata
# target_metadata = Base.metadata

# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode."""
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()

# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode."""
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()

# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import your models
from git_day_practice.db import Base
import git_day_practice.models

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()