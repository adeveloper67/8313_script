from django.db import models


from django.db import models


class Prompts(models.Model):
    prompt = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt

    class Meta:
        verbose_name = 'Prompt'
        verbose_name_plural = 'Prompts'
