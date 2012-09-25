from django.db import models

class Finance_Info(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_user_id =  models.IntegerField()
    c_pay_time = models.DateTimeField()
    c_pay_amount = models.IntegerField()
    c_expired_dates =models.IntegerField()
    class Meta:
        db_table = u't_finance_info'

class User(models.Model):
    c_user_id = models.IntegerField(primary_key=True)    
    c_user_name = models.CharField(max_length=40)
    c_password = models.CharField(max_length=40)
    c_company_name = models.CharField(max_length=40)
    c_sex =  models.IntegerField()
    c_real_name = models.CharField(max_length=40)
    c_id_card_no =  models.CharField(max_length=20) 
    c_phone_no = models.CharField(max_length=20)
    c_email_addr =  models.CharField(max_length=40)
    c_register_time= models.DateTimeField()
    c_count_state= models.IntegerField()
    c_expired_time= models.DateTimeField()
    c_last_login_time =  models.DateTimeField()
    c_online_state  = models.IntegerField()
    c_level =  models.IntegerField()
    c_type = models.IntegerField()
    class Meta:
        db_table = u't_user_info'

class Login_Randint(models.Model):
    c_id = models.IntegerField(primary_key=True)    
    c_user_name = models.CharField(max_length=40)
    c_randint = models.IntegerField()
    class Meta:
        db_table = u't_login_randint'

class User_Action_Log(models.Model):
    c_id = models.IntegerField(primary_key=True)    
    c_user_id = models.CharField(max_length=40)
    c_action_type = models.IntegerField()
    c_action_time = models.DateTimeField(auto_now_add=True)
    c_action_result = models.IntegerField()
    class Meta:
        db_table = u't_user_action_log'

class Client_Amount(models.Model):
    c_id = models.IntegerField(primary_key=True)
    client_type= models.CharField(max_length=40)
    date =models.DateField()
    amount= models.IntegerField()
    class Meta:
        db_table = u'client_amount'


