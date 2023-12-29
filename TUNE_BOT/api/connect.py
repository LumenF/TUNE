from api.methods.Logs import LogsApi
from api.methods.favorite import FavoriteApi
from api.methods.mailing import MailingApi
from api.methods.new import NewProductApi
from api.methods.user import UserApi
from api.methods.supp import SuppProductApi


class APIServer(
    UserApi,
    SuppProductApi,
    FavoriteApi,
    NewProductApi,
    MailingApi,
    LogsApi
):
    pass
