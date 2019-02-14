from django.db import models

# Create your models here.


# 用户模型
class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    sex = models.IntegerField(null=True)
    email = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=11)
    pic = models.CharField(max_length=100)
    # 0正常 1禁用 2删除
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_users", "查看会员管理"),
            ("insert_users", "添加会员"),
            ("edit_users", "修改会员"),
            ("del_users", "删除会员"),
        )


# 分类模型
class Types(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)
    pname = models.CharField(max_length=20)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_types", "查看商品分类管理"),
            ("insert_types", "添加商品分类"),
            ("edit_types", "修改商品分类"),
            ("del_types", "删除商品分类"),
        )


# 商品模型
class Goods(models.Model):
    tid = models.ForeignKey(to="Types", to_field="id")
    title = models.CharField(max_length=255)
    price = models.FloatField()
    num = models.IntegerField()
    info = models.TextField()
    pic = models.CharField(max_length=255)
    # 0 新发布  1,热卖   2,下架  3,删除
    status = models.IntegerField()
    clicknum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_goods", "查看商品管理"),
            ("insert_goods", "添加商品"),
            ("edit_goods", "修改商品"),
            ("del_goods", "删除商品"),
        )


# 购物车模型
class CartGoods(models.Model):
    uid = models.ForeignKey(to=Users, to_field='id')
    goodsid = models.IntegerField()
    num = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)


# 收货地址
class Address(models.Model):
    uid = models.ForeignKey(to='Users', to_field='id')
    addresspreson = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    addressphone = models.CharField(max_length=11)
    # 状态  0-普通地址  1-默认地址  2-已删除地址
    status = models.IntegerField(default=0)


# 用户订单
class UserOrder(models.Model):
    uid = models.ForeignKey(to='Users', to_field='id')
    addressid = models.IntegerField()
    totalprice = models.FloatField()
    addtime = models.DateTimeField(auto_now_add=True)
    # 订单状态  0未付款  1已付款  2已完成  3已取消
    status = models.IntegerField(default=0)

    class Meta:
        # 指定生成权限
        permissions = (
            ("show_orders", "查看订单管理"),
            ("del_orders", "删除订单"),
        )


# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="UserOrder", to_field="id")
    goodsid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()
    price = models.FloatField()




