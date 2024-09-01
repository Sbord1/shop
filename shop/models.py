import boto3
from io import BytesIO
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.URLField(max_length=200)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    local_image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.local_image:
            s3 = boto3.client('s3')
            buffer = BytesIO()
            self.local_image.open()
            image_content = self.local_image.read()
            buffer.write(image_content)
            buffer.seek(0)
            s3.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=f'{settings.AWS_LOCATION}/{self.local_image.name}',
                Body=buffer,
                ContentType=self.local_image.file.content_type
            )
            self.image = f'https://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_LOCATION}/{self.local_image.name}'
            self.local_image = None

        super().save(*args, **kwargs)
