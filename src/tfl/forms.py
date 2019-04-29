from django import forms
from django.forms.widgets import Input, CheckboxInput, ClearableFileInput
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
# from django.utils.encoding import force_unicode


class MyImageWidget(forms.widgets.ClearableFileInput):
     template_name = "upload/upload_form.html"

     # def render(self, name, value, attrs=None, renderer=None):
     #      # print(value)
     #      # print(name)
     #      print(self.template_name)




     # def render(self, name, value, attrs=None, renderer=None):
     #      substitutions = {
     #           # uncomment to get 'Currently'
     #           'initial_text': "",  # self.initial_text,
     #           'input_text': self.input_text,
     #           'clear_template': '',
     #           'clear_checkbox_label': self.clear_checkbox_label,
     #      }
     #      template = '%(input)s'
     #      substitutions['input'] = Input.render(self, name, value, attrs)
     #
     #      if value and hasattr(value, "url"):
     #           print('usloooooo')
     #           template = self.template_name
     #           substitutions['initial'] = ('<img src="%s" alt="%s"/>'
     #                                       % (escape(value.url),
     #                                          escape(force_text(value))))
     #           print(self.is_required)
     #           if not self.is_required:
     #                checkbox_name = self.clear_checkbox_name(name)
     #                checkbox_id = self.clear_checkbox_id(checkbox_name)
     #                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
     #                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
     #                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
     #                substitutions['clear_template'] = self.template_with_clear % substitutions
     #
     #      return mark_safe(template % substitutions)

     # def render(self, name, value, attrs=None, renderer=None):
     #      template = '%(input)s'
     #      data = {'input': None, 'url': None}
     #      data['input'] = super(MyImageWidget, self).render(name, value, attrs)
     #
     #      if hasattr(value, 'url'):
     #           data['url'] = conditional_escape(value.url)
     #           template = '%(input)s <img src="%(url)s">'
     #
     #      return mark_safe(template % data)

     # def __init__(self, *args, **kwargs):
     #
     #      self.url_length = kwargs.pop('url_length', 30)
     #      self.preview = kwargs.pop('preview', True)
     #      self.image_width = kwargs.pop('image_width', 200)
     #      super(MyImageWidget, self).__init__(*args, **kwargs)
     #
     # def render(self, name, value, attrs=None, renderer=None):
     #
     #      substitutions = {
     #           'initial_text': self.initial_text,
     #           'input_text': self.input_text,
     #           'clear_template': '',
     #           'clear_checkbox_label': self.clear_checkbox_label,
     #      }
     #      template = u'%(input)s'
     #
     #
     #      substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)
     #
     #      print(substitutions)
     #
     #      if value and hasattr(value, "url"):
     #
     #           # template = self.template_name
     #           # template = u'%(input)s'
     #           if self.preview:
     #                substitutions['initial'] = (u'<a href="{0}">{1}</a><br>\
     #              <a href="{0}" target="_blank"><img src="{0}" width="{2}"></a><br>'.format
     #                                            (escape(value.url),
     #                                             '...' + escape(force_text(value))[-self.url_length:],
     #                                             self.image_width))
     #           else:
     #                substitutions['initial'] = (u'<a href="{0}">{1}</a>'.format
     #                                            (escape(value.url),
     #                                             '...' + escape(force_text(value))[-self.url_length:]))
     #           if not self.is_required:
     #                checkbox_name = self.clear_checkbox_name(name)
     #                checkbox_id = self.clear_checkbox_id(checkbox_name)
     #                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
     #                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
     #                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
     #                substitutions['clear_template'] = self.template_name % substitutions
     #
     #      return mark_safe(template % substitutions)