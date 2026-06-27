from django.db import migrations, models


def add_order_email(apps, schema_editor):
    Order = apps.get_model('shop', 'Order')
    table_name = Order._meta.db_table
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        try:
            description = connection.introspection.get_table_description(cursor, table_name)
            columns = [getattr(column, 'name', column[0]) for column in description]
        except Exception:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]

        if 'email' not in columns:
            field = models.EmailField(blank=True, null=True, max_length=254)
            field.set_attributes_from_name('email')
            field.model = Order
            schema_editor.add_field(Order, field)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order_email'),
    ]

    operations = [
        migrations.RunPython(add_order_email, reverse_code=migrations.RunPython.noop),
    ]
