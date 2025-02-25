from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import BlogComment


class CommentAdmin(ModelAdmin):
    model = BlogComment
    base_url_path = "blogcomment"  # customise the URL from default to admin/bookadmin
    menu_label = "Blog Comment"  # ditch this to use verbose_name_plural from model
    menu_icon = "pilcrow"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ("post", "name", "body")
    list_filter = ("post", "body")
    search_fields = ("post", "body")


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(CommentAdmin)
