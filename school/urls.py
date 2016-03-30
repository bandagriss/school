from django.conf.urls import include, url
from django.contrib import admin
from usuario.views import OrderListJson

urlpatterns = [
    # Examples:
    # url(r'^$', 'school.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #usuario
    url(r'^usuario/ver/(?P<id>\d+)', 'usuario.views.show', name="detalle"),
    url(r'^usuario/editar/(?P<id>\d+)', 'usuario.views.edit'),
    url(r'^usuario/update/(?P<id>\d+)', 'usuario.views.update'),
    url(r'^usuario/index/$', 'usuario.views.index'),
    url(r'^datatable/usuario/$', OrderListJson.as_view(), name='order_list_json'),

    #cuenta
    url(r'^$', 'cuenta.views.login'),
    url(r'^crear/$', 'cuenta.views.crear'),
    url(r'^registrar/$', 'cuenta.views.register_account'),
    url(r'^autenticacion/$', 'cuenta.views.auth_view'),
    url(r'^logout/$', 'cuenta.views.cerrar'),
    url(r'^inicio/$', 'cuenta.views.home'),

    #libro
    url(r'^sms/$', 'libro.views.IndexSms'),
    url(r'^twiliosms/$', 'libro.views.twiliosms'),
    url(r'^libro/index/$', 'libro.views.index'),

    #
]
