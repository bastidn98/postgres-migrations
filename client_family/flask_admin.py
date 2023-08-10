from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for

class HomePageRedirect(AdminIndexView):
    @expose("/")
    def index(self):
        return redirect(url_for("client_family.index_view"))

class ClassFamilyModelView(ModelView):
    pass