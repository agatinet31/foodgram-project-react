from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрациия пользователя."""
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения данных пользователя."""
    subscribed = ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            _('subscribed'),
            is_stacked=False
        )
    )
    subscribers = ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            _('subscribers'),
            is_stacked=False
        )
    )

    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['subscribed'] = ModelMultipleChoiceField(
                queryset=CustomUser.objects.all().exclude(pk=self.instance.pk),
                required=False,
                widget=FilteredSelectMultiple(
                    verbose_name='subscribed',
                    is_stacked=False
                )
            )
            self.fields['subscribers'] = ModelMultipleChoiceField(
                queryset=CustomUser.objects.all().exclude(pk=self.instance.pk),
                required=False,
                widget=FilteredSelectMultiple(
                    verbose_name='subscribers',
                    is_stacked=False
                )
            )
            subscribers = self.instance.subscribers.all()
            self.fields['subscribers'].initial = subscribers
