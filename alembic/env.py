from __future__ import with_statement

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

from app.postgres.database import Base

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_url():
    """
    Obtém a URL de conexão com o banco de dados a partir das variáveis de ambiente.

    A função lê a variável de ambiente 'DATABASE_URL' e retorna seu valor. Esta URL
    é utilizada para conectar ao banco de dados durante o processo de migração.

    Returns:
        str: URL de conexão com o banco de dados.
    """
    return os.getenv("DATABASE_URL")


def run_migrations_offline():
    """
    Executa as migrações no modo offline.

    No modo offline, as migrações são realizadas usando a URL do banco de dados diretamente,
    e as instruções SQL são geradas e aplicadas diretamente sem uma conexão ativa com o banco
    de dados.

    As migrações são executadas em uma transação, garantindo que as operações de migração
    sejam atômicas.
    """
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Executa as migrações no modo online.

    No modo online, uma conexão com o banco de dados é estabelecida e as migrações são
    realizadas através dessa conexão. Isso permite que as migrações sejam aplicadas de
    maneira dinâmica e interativa.

    A configuração do banco de dados é feita a partir das configurações do arquivo de configuração
    e a conexão é gerenciada com o pool de conexões `NullPool` para evitar o uso de cache de
    conexões.

    As migrações são executadas em uma transação para garantir a integridade das operações.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url()
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
