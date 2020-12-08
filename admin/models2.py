from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.

class member_tbl(models.Model):
    # member_number = models.AutoField(primary_key=True)
    member_join_date = models.DateTimeField(auto_now=True)
    member_manager = models.BooleanField(null=False, default=False)
    member_total_price = models.IntegerField(default=0)
    member_rank = models.CharField(max_length=20)
    member_password = models.CharField(max_length=15)
    member_id = models.CharField(max_length=18)
    member_contact_number = models.IntegerField()
    member_name = models.CharField(max_length=20)
    member_email = models.CharField(max_length=50)
    member_address = models.CharField(max_length=100)
    # slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        db_table = 'admin_member_tbl'
    #     index_together = [['member_number', 'slug']]
    #
    # def __str__(self):
    #     return self.name
    #
    # def get_absolute_url(self):
    #     return reverse('member:member_detail', args=[self.member_number, self.slug])




class product_tbl(models.Model):
    product_number = models.AutoField(primary_key=True)

    product_Price = models.IntegerField(null=False)
    product_register_date = models.DateTimeField(auto_now=True)
    product_made_date = models.CharField(max_length=20)
    product_name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    product_image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    product_description = models.CharField(max_length=1000, blank=True)
    product_volume = models.IntegerField(db_index=True)
    product_stock = models.PositiveIntegerField()
    product_category = models.CharField(max_length=20)
    product_size = models.CharField(max_length=20)
    product_brand = models.CharField(max_length=20)
    product_manufacturer = models.CharField(max_length=20)
    product_meterial = models.CharField(max_length=20)
    product_made_country = models.CharField(max_length=20)
    class Meta:
        index_together = [['product_number', 'slug']]

    def product_save(self):
        self.save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.product_number, self.slug])



class order_tbl(models.Model):
    order_number = models.AutoField(primary_key=True)
    member_number = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    product_number = models.ForeignKey(product_tbl, on_delete=models.CASCADE)
    order_price = models.IntegerField()
    order_pay_status = models.CharField(max_length=10)
    order_mathod = models.CharField(max_length=2)
    order_quantity = models.IntegerField()
    order_transport_number = models.CharField(max_length=50)
    order_bank = models.CharField(max_length=14)
    order_deposit_person = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=6)
    order_delivery_company = models.CharField(max_length=20)

    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        index_together = [['order_number', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order:order_detail', args=[self.order_number, self.slug])


class cart_tbl(models.Model):
    cart_number = models.AutoField(primary_key=True)
    member_number = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    product_number = models.ForeignKey(product_tbl, on_delete=models.CASCADE)
    cart_discount = models.IntegerField()
    cart_delivery_price = models.IntegerField()
    cart_product_price = models.IntegerField()
    cart_quantity = models.IntegerField()

    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        index_together = [['cart_number', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cart:cart_detail', args=[self.cart_number, self.slug])


class m2mfaq_tbl(models.Model):
    # comment_number = models.AutoField(primary_key=True)
    member_number = models.ForeignKey(member_tbl, on_delete=models.CASCADE)
    comment_status = models.CharField(max_length=1)
    comment_image = models.ImageField(upload_to='m2m/%Y-%m-%d', max_length=100)
    comment_write_date = models.DateTimeField(auto_now=True)
    comment_title = models.CharField(max_length=50)
    comment_question = models.CharField(max_length=1000)
    comment_category = models.CharField(max_length=10)

    # slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    #
    class Meta:
        db_table = 'admin_m2mfaq_tbl'
    #     index_together = [['comment_number', 'slug']]
    #
    # def __str__(self):
    #     return self.name
    #
    def get_absolute_url(self):
        return reverse('admin:m2m_answer', args=[self.id])

    def get_image_url(self):
        return '%s%s' %(settings.MEDIA_URL, self.comment_image)

class faq_answer_tbl(models.Model):
    answer_number = models.AutoField(primary_key=True)
    comment_number = models.ForeignKey(m2mfaq_tbl, on_delete=models.CASCADE)
    answer_description = models.CharField(max_length=1000)
    answer_write_date = models.DateTimeField(auto_now=True)
    # answer_write_date = m2mfaq_tbl.comment_write_date
    answer_writer = models.CharField(max_length=3, default='관리자')


    # slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    #
    class Meta:
        db_table = 'admin_faq_answer_tbl'

    #     index_together = [['answer_number', 'slug']]
    #
    # def __str__(self):
    #     return self.name
    #
    def get_absolute_url(self):
        return reverse('admin:m2m_answer', args=[self.id])


class address_tbl(models.Model):
    address_road_name = models.CharField(max_length=10)
    address_road_code = models.IntegerField()
    address_si_gun_gu = models.CharField(max_length=10)
    address_si_do = models.CharField(max_length=10)
    address_post_number = models.IntegerField()

