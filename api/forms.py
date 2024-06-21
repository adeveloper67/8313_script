from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)

        # Validate file types
        for file in result:
            if file.content_type not in ['application/pdf', 'text/plain']:
                raise forms.ValidationError(
                    'File type not supported. Only PDF and TXT files are allowed.'
                )

        return result


class UploadForm(forms.Form):
    prompt = forms.CharField(max_length=255, required=True)
    files = MultipleFileField(required=True)
