from django import forms
from .models import Product

# Список запрещённых слов
BANNED_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

def contains_banned_words(value):
    """
    Проверяет, содержит ли строка запрещённые слова как отдельные слова (без учёта регистра).
    """
    import re
    if not value:
        return
    value_lower = value.lower()
    for word in BANNED_WORDS:
        if re.search(rf'\b{re.escape(word)}\b', value_lower):
            raise forms.ValidationError(f"Слово '{word}' запрещено к использованию.")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'purchase_price']
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'purchase_price': 'Цена за покупку',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Применяем Bootstrap-классы ко всем полям
        for field_name, field in self.fields.items():
            # Добавляем класс form-control ко всем полям
            field.widget.attrs['class'] = 'form-control'

            # Для поля изображения — можно оставить как есть (или добавить custom стиль)
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'

            # Для текстовых полей и чисел — можно добавить placeholder
            if field_name in ['name', 'purchase_price']:
                field.widget.attrs['placeholder'] = f'Введите {field.label.lower()}...'

            # Для описания — можно добавить подсказку
            if field_name == 'description':
                field.widget.attrs['placeholder'] = 'Описание товара (не используйте запрещённые слова)...'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            contains_banned_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            contains_banned_words(description)
        return description

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
