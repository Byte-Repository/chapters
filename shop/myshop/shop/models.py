from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields  # type: ignore
from django.contrib.auth.models import User
from recipe.models import Post 
from django.utils import timezone

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200),
        slug = models.SlugField(max_length=200, unique=True),
    )

    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200),
        description=models.TextField(blank=True),
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # New fields
    is_subscription = models.BooleanField(default=False)
    subscription_duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in days for subscriptions")
    is_recipe_book = models.BooleanField(default=False)
    related_recipes = models.ManyToManyField(Post, related_name='products', blank=True)

    class Meta:
        # ordering = ['name']
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
class Subscription(models.Model):
    TIER_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    tier = models.CharField(max_length=50, choices=TIER_CHOICES)

    def is_active(self):
        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.username} - {self.get_tier_display()} subscription"