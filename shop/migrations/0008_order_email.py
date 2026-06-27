from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
