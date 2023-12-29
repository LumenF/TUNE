import ast
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv()
PRODUCTION = ast.literal_eval(os.getenv('PRODUCTION'))
if PRODUCTION:
    ENV = find_dotenv(filename='.prod.env')
    print('START PRODUCTION SCRIPT')
else:
    ENV = find_dotenv(filename='.dev.env')
    print('START DEVELOPMENT SCRIPT')
load_dotenv(ENV)


import middleware.auth as auth_middleware
import app.index.func as index
import app.product.func as product
import app.supproduct.func as supproduct
import app.budget.func as budget
import app.sale.func as sale
import app.trade.func as trade
import app.user.func as user


########################################################################
# Всегда внизу!!!
import app.bitrix.func as bitrix
########################################################################

