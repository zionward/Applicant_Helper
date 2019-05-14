"""
This module creates TD prediction database and table using defined db in SQLAlchemy.
Configuration parameter in __init__.py with the schema defined by td_app.db_model.TD
"""

from td_app import db
import logging


def create_db():
    """
    Function that creates initial database
    Args:
    Returns:
    """
    db.drop_all()
    logger.info('Cleared previous database records.')

    db.create_all()
    logger.info('Database initialization successful.')

    try:
        db.session.commit()
        logger.info('Database successfully committed.')
    except :
        logger.info('Database commit error.')


if __name__ == "__main__":
    # logger initialization
    logging.basicConfig(filename="create_db.log",
                        level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")
    logger = logging.getLogger(__name__)
    create_db()