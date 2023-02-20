from datetime import datetime

from django.contrib.admin.widgets import AdminFileWidget, FilteredSelectMultiple
from django.db import models
from django.utils.safestring import mark_safe

from abstractions.preview.image_preview import preview

from django.contrib import admin


class AdminImageWidget(AdminFileWidget):
    """
    Виджет изображения для formfield_overrides
    """

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(preview(image_url))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class AdminManyToManyWidget(FilteredSelectMultiple):
    """
    Виджет ManyToMany для formfield_overrides
    """

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(preview(image_url))
        output.append(super(FilteredSelectMultiple, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class AbstractAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {
            'widget': AdminImageWidget
        },
        # models.ManyToManyField: {
        #     'widget': AdminManyToManyWidget
        # }
    }
    exclude = (
        'author',
    )

    def save_model(self, request, obj, form, change):
        user = request.user
        obj.author = user
        if not change:
            obj.user_ptr_id = 1
            obj.date_created = datetime.utcnow()
            obj.date_last_modified = datetime.utcnow()
        obj.save()


def get_path(path: str):
    if path.split('/')[1] in ['actual_params', 'product_params', 'params', 'region', 'params_automobile']:
        settings_path = [
            'region',
            'params',
            'params_automobile',
            'product_params',
            'actual_params',
        ]
        return settings_path

    if path.split('/')[1] in ['auth', 'user', 'cart', ]:
        company_path = [
            'auth',
            'user',
            'cart',
        ]
        return company_path

    if path.split('/')[1] in ['product_new', 'product_supp', 'product_automobile']:
        settings_path = [
            'product_new',
            'product_supp',
            'product_automobile',
        ]
        return settings_path

    if path.split('/')[1] in ['bot_params', ]:
        settings_path = [
            'bot_params',
        ]
        return settings_path

    if path.split('/')[1] in ['repair', ]:
        settings_path = [
            'repair',
        ]
        return settings_path

    if path.split('/')[1] in ['provider', ]:
        settings_path = [
            'provider',
        ]
        return settings_path

    if path.split('/')[1] in ['manager', ]:
        settings_path = [
            'manager',
        ]
        return settings_path
    return [
        'product_new',

    ]


def app_resort(func):
    def inner(*args, **kwargs):
        app_list = func(*args, **kwargs)
        path_list = get_path(args[0].path)
        app_sort_key = 'name'
        app_ordering = {
        }
        resorted_app_list = sorted(app_list,
                                   key=lambda x: app_ordering[x[app_sort_key]]
                                   if x[app_sort_key] in app_ordering else 1000)

        resorted_app_list = [i for i in resorted_app_list if i['app_label'] in path_list]
        model_sort_key = 'object_name'
        model_ordering = {
            "ManufacturerModel": 1,
            "GroupModel": 2,
            "DeviceModel": 3,
            "SeriesModel": 4,
            "ParameterModel": 5,
            "WordsModel": 6,
            "RegionModel": 7,
            "CityModel": 8,

            "AutomobileModel": 9,
            "ManufacturerAutomobileModel": 10,
        }
        for app in resorted_app_list:
            app['models'].sort(
                key=lambda x: model_ordering[x[model_sort_key]] if x[model_sort_key] in model_ordering else 1000)
        return resorted_app_list

    return inner


# admin.site.get_app_list = app_resort(admin.site.get_app_list)
