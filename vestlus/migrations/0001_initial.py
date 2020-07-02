# Generated by Django 2.2.12 on 2020-05-27 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('access_code', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='access code')),
                ('is_private', models.BooleanField(default=True, verbose_name='is private')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='channels', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'db_table': 'vestlus_channels',
                'ordering': ['-created_at', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='uploaded at')),
                ('parent', models.ForeignKey(blank=True, help_text='The main message in a message thread', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='vestlus.Message', verbose_name='parent')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_vestlus.message_set+', to='contenttypes.ContentType')),
                ('sender', models.ForeignKey(help_text='The user who authored the message', on_delete=django.db.models.deletion.PROTECT, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'db_table': 'vestlus_messages',
                'ordering': ['-created_at', 'sender'],
            },
        ),
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vestlus.Message')),
            ],
            options={
                'db_table': 'vestlus_group_messages',
                'ordering': ['-created_at', 'channel'],
            },
            bases=('vestlus.message',),
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(help_text='Emoji reaction code as unicode', max_length=32, verbose_name='reaction')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='uploaded at')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='vestlus.Message', verbose_name='message')),
                ('user', models.ForeignKey(help_text='The user who reacted to the message', on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'db_table': 'vestlus_message_reactions',
                'ordering': ['-created_at', 'message', 'user'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False, help_text='Defines if user has admin privileges', verbose_name='is admin')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='uploaded at')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='vestlus.Channel', verbose_name='channel')),
                ('invited_by', models.ForeignKey(blank=True, help_text='The user who invited this one', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invitees', to=settings.AUTH_USER_MODEL, verbose_name='invited by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'db_table': 'vestlus_channel_members',
                'ordering': ['-created_at', 'user'],
            },
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vestlus.Message')),
                ('read', models.BooleanField(default=False, help_text='Indicates whether or not the recipient has visualized the message', verbose_name='read')),
                ('receiver', models.ForeignKey(blank=True, help_text='The user this message will be sent to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='receiver')),
            ],
            options={
                'db_table': 'vestlus_private_messages',
            },
            bases=('vestlus.message',),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['created_at', 'sender', 'parent'], name='vestlus_mes_created_891831_idx'),
        ),
        migrations.AddIndex(
            model_name='membership',
            index=models.Index(fields=['channel', 'user', 'invited_by', 'slug', 'created_at'], name='vestlus_cha_channel_b4cdf7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('channel', 'user')},
        ),
        migrations.AddField(
            model_name='groupmessage',
            name='channel',
            field=models.ForeignKey(help_text='The channel associated with this message', on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='vestlus.Channel', verbose_name='channel'),
        ),
        migrations.AddIndex(
            model_name='channel',
            index=models.Index(fields=['name', 'owner', 'slug', 'created_at'], name='vestlus_cha_name_8c4e10_idx'),
        ),
        migrations.AddIndex(
            model_name='privatemessage',
            index=models.Index(fields=['receiver', 'read'], name='vestlus_pri_receive_6188e6_idx'),
        ),
        migrations.AddIndex(
            model_name='groupmessage',
            index=models.Index(fields=['channel'], name='vestlus_gro_channel_64ddc1_idx'),
        ),
    ]