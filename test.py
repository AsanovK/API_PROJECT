"""


djangorestframework-simplejwt - регистрация на другой основе
отличие от предыдущего проекта:
1) письмо на телефон 
2) сэлэри 
3) логин на других токенов(jwt tokens)



в инсталд аппс вторым передаем
    'rest_framework_simplejwt',


 Настраиваем .env 
TWILIO_SID=ACd86d0bdbe5407e6a41f28501c13630fd
TWILIO_TOKEN=7c0162fb617f3d001227d533fa11b53f
TWILIO_NUMBER=

celery -A config(название приложение) worker -l INFO


pyhton3 manage.py shell

from config.celery import add
task = add.delay

if:  TwilioRestException at /account/register

write in serializers.py   .delay
send_activation_sms.delay(user.phone, user.activation_code)
"""

# APIVIEW сами
# genericView дополняем 
# ModelViewSet все 4 метода уже определены