from django import forms


class MyImageWidget(forms.widgets.ClearableFileInput):
     template_name = "upload/upload_form.html"
     is_required = True
