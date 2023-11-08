from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_admin.form.fields import Select2Field
from flask import redirect, url_for
from .clients import make_client_choices
from .models import ClientFamily

class HomePageRedirect(AdminIndexView):
    @expose("/")
    def index(self):
        return redirect(url_for("client_family.index_view"))

class ClassFamilyModelView(ModelView):
    column_list = sum(ClientFamily.get_fieldnames(), [])
    column_filters = column_list.copy()
    form_columns = ['client', 'family_head']
    form_overrides = {"client": Select2Field, "family_head": Select2Field} 

    def create_form(self, obj=None):
        form = super().create_form(obj)
        choices = make_client_choices()
        form.client.choices = choices
        form.family_head.choices = choices
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        choices = make_client_choices()
        form.client.choices = choices
        form.family_head.choices = choices
        return form

    def on_model_change(self, form, model, is_created):
        client_code, client_name= form.client.data.split('-')
        model.client = client_code
        model.client_name = client_name

        family_head_code, family_head_name= form.family_head.data.split('-')
        model.family_head = family_head_code
        model.family_head_name = family_head_name

        return super(ClassFamilyModelView, self).on_model_change(form, model, is_created)

    