from mod.user_agreement.user_agreement import  UserAgreementHandler
from mod.user.user import UserHandler
from mod.user.find import FindHandler
from mod.user.change_pwd import ChangePwdHandler
from mod.login.login import LoginHandler
from mod.login.relogin import ReLoginHandler
from mod.user.changenick import ChangenickHandler
from mod.goods.listgoods import ListGoodsHandler
from mod.goods.get_food_kind_1st import GetFoodKind1stHandler
from mod.address.add_address import AddAddressHandler
from mod.address.change_address import ChangeAddressHandler
from mod.address.delete_address import DeleteAddressHandler
from mod.address.get_address import GetAddressHandler
from mod.market.listmarket import ListMarketsHandler
from mod.order.add_order import AddOrderHandler
from mod.order.list_order import ListOrderHandler
from mod.order.order_detail import OrderDetailHandler
from mod.order.order_statue import OrderStatueHandler
from mod.order.delete_order import DeleteOrderHandler
from mod.order.confirm_order import ConfirmOrderHandler
from mod.order.cancel_order import CancelOrderHandler
from mod.order.evaluate_order import EvaluateOrderHandler
from mod.order.get_evaluation import GetEvaluationHandler

handlers=(
    (r'/bangzai/user_agreement', UserAgreementHandler),
    (r'/bangzai/user',UserHandler),
    (r'/bangzai/login',LoginHandler),
    (r'/bangzai/relogin',ReLoginHandler),
    (r'/bangzai/user/find',FindHandler),
    (r'/bangzai/user/change_pwd',ChangePwdHandler),
    (r'/bangzai/user/changenick',ChangenickHandler),
    (r'/bangzai/goods/listgoods',ListGoodsHandler),
    (r'/bangzai/goods/get_food_kind_1st',GetFoodKind1stHandler),
    (r'/bangzai/address/add_address',AddAddressHandler),
    (r'/bangzai/address/change_address',ChangeAddressHandler),
    (r'/bangzai/address/delete_address',DeleteAddressHandler),
    (r'/bangzai/address/get_address',GetAddressHandler),
    (r'/bangzai/market/listmarket',ListMarketsHandler),
    (r'/bangzai/order/add_order',AddOrderHandler),
    (r'/bangzai/order/list_order',ListOrderHandler),
    (r'/bangzai/order/order_detail',OrderDetailHandler),
    (r'/bangzai/order/order_status',OrderStatueHandler),
    (r'/bangzai/order/delete_order',DeleteOrderHandler),
    (r'/bangzai/order/confirm_order',ConfirmOrderHandler),
    (r'/bangzai/order/cancel_order',CancelOrderHandler),
    (r'/bangzai/order/evaluate_order',EvaluateOrderHandler),
    (r'/bangzai/order/get_evaluation',GetEvaluationHandler),
)
