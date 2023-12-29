from __future__ import absolute_import
from TUNE.celery_conf import app as celery_app
import pymysql

pymysql.install_as_MySQLdb()
pymysql.version_info = (2, 1, 1, "final", 0)

__all__ = ('celery_app',)
