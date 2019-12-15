"""kg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
# from django.shortcuts import HttpResponse,render
from .import index,knowledge,relation_view,relation,question_answering
urlpatterns = [
    url(r'^$', index.new_index),
    url(r'^knowledge', knowledge.knowledge),
    url(r'^rel', relation.rel),
    url(r'^QA', question_answering.qa),
    url(r'^search_entity',relation_view.search_entity),
    url(r'^searchRelationForm', relation_view.search_relation),
]
