import uuid

from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_created_by',
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_modified_by',
    )
    deleted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_deleted_by',
    )

    class Meta:
        abstract = True


class Driver(BaseModel):
    name = models.TextField(max_length=150)
    email = models.EmailField()
    address = models.TextField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Vehicle(BaseModel):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)

    brand = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    serial_number = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.brand} - {self.model} - {self.serial_number}'

    @property
    def driver_name(self):
        return self.driver.name


class InsuranceApplication(BaseModel):
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    WAITING = "WAITING"

    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (WAITING, 'Waiting for approval')
    )

    drivers = models.ManyToManyField(Driver)
    review_date = models.DateField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Waiting for approval')

    def __str__(self) -> str:
        return f'{self.status}'

    @property
    def sub_date(self):
        # Submission Date
        return f'{self.created_at}'

