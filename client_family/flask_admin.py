import pickle
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_admin.form.fields import Select2Field
from flask_admin.contrib.sqla import filters
from wtforms.fields import HiddenField

from flask import redirect, url_for, flash, session
from .clients import make_client_choices, client_code_domain_dict
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
    can_edit = False
    create_template = 'create_with_check.html' 
    can_export = True
    export_types = ['csv']

    def create_form(self, obj=None):
        form = super().create_form(obj)
        choices = make_client_choices()
        # with open('choices.pkl', 'rb') as f:
        #     choices = pickle.load(f)
        form.client.choices = choices
        form.family_head.choices = choices
        return form

    def create_form(self, obj=None):
        form = super().create_form(obj)
        choices = make_client_choices()
        form.client.choices = choices
        form.family_head.choices = choices
        form.confirmed = HiddenField(default='no')  # Add a hidden field for confirmation
        return form

    def on_model_change(self, form, model, is_created):
        client_code, client_name= form.client.data.split(':')
        model.client = client_code
        model.client_name = client_name

        family_head_code, family_head_name= form.family_head.data.split(':')
        model.family_head = family_head_code
        model.family_head_name = family_head_name

        return super(ClassFamilyModelView, self).on_model_change(form, model, is_created)

    def get_list(self, page, sort_column, sort_desc, search, filters, execute=True, page_size=None):
        flash('Instead of editing, please delete and re-create')
        return super().get_list(page, sort_column, sort_desc, search, filters, execute, page_size)

    