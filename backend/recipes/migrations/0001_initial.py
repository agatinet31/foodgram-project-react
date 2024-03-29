# Generated by Django 2.2.16 on 2022-09-13 09:26

import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'A ingredient with that name already exists.'}, help_text='Required. Enter ingredient name, please. 250 characters or fewer. Letters, digit symbols _ ( " ). The first symbol only letter.', max_length=250, validators=[django.core.validators.RegexValidator(re.compile('^#?[\\w]+$'), 'Enter a valid `name` value consisting of only letters, digit. and symbols _ ( )The first symbol only letter.', 'invalid')], verbose_name='name')),
                ('measurement_unit', models.CharField(help_text='Required. Enter measurement_unit, please.', max_length=50, validators=[django.core.validators.RegexValidator(re.compile('^[^\\W\\d_]+$'), 'Enter a valid string value consisting of only letters.', 'invalid')], verbose_name='measurement_unit')),
            ],
            options={
                'verbose_name': 'ingredient',
                'verbose_name_plural': 'ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. Enter name recipe, please.', max_length=500, validators=[django.core.validators.RegexValidator(re.compile('^#?[\\w]+$'), 'Enter a valid `name` value consisting of only letters, digit. and symbols _ ( )The first symbol only letter.', 'invalid')], verbose_name='name')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='public date')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='image')),
                ('text', models.TextField(verbose_name='recipe text')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Minimum cooking time 1 minute')], verbose_name='cooking_time')),
                ('author', models.ForeignKey(help_text='Required. Enter author, please. ', on_delete=django.db.models.deletion.CASCADE, related_name='author_recipes', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='favorites')),
            ],
            options={
                'verbose_name': 'recipe',
                'verbose_name_plural': 'recipes',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'A tag with that name already exists.'}, help_text='Required. Enter tag name, please. 150 characters or fewer. Letters, digit onlyand first symbol can be `#`', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^#?[\\w]+$'), 'Enter a valid `tag` value consisting of only letters, digit. The first symbol can be `#`.', 'invalid')], verbose_name='name')),
                ('color', models.CharField(error_messages={'unique': 'A tag with that color already exists.'}, help_text='Required. Enter HEX-code color, please.', max_length=7, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'), 'The valid hexadecimal color code must satisfy the following conditions:1. It should start from ‘#’ symbol.2. It should be followed by the letters from a-f, A-F and/or digits from 0-9.3. The length of the hexadecimal color code should be either 6 or 3, excluding ‘#’ symbol.', 'invalid')], verbose_name='color HEX-code')),
                ('slug', models.SlugField(error_messages={'unique': 'A tag with that slug already exists.'}, help_text='Required. Enter slug tag, please.', unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='The minimum quantity of an ingredient in a recipe is 1')], verbose_name='amount')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.Ingredient', verbose_name='ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.Recipe', verbose_name='recipe')),
            ],
            options={
                'verbose_name': 'recipe ingredient',
                'verbose_name_plural': 'recipe ingredients',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, related_name='recipes', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='shopping_carts',
            field=models.ManyToManyField(blank=True, related_name='shopping_cart_recipes', to=settings.AUTH_USER_MODEL, verbose_name='shopping_carts'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipes.Tag', verbose_name='tags'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['name'], name='recipe_name_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['text'], name='recipe_text_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['pub_date'], name='recipe_pub_date_idx'),
        ),
    ]
