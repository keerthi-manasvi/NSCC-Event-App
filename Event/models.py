from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
import uuid
from django.core.validators import EmailValidator

class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

def gen_reg_id():
    return uuid.uuid4().hex[:8].upper()

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    registration_id = models.CharField(max_length=50, unique=True, default=gen_reg_id)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.qr_code_image:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(self.registration_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save to ImageField
            blob = BytesIO()
            img.save(blob, 'PNG')
            self.qr_code_image.save(f'{self.registration_id}.png', File(blob), save=False)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} ({self.registration_id})"

class Attendance(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, related_name='attendance')
    timestamp = models.DateTimeField(default=timezone.localtime)
    status = models.CharField(max_length=20, default='Present')

    def __str__(self):
        local_time = timezone.localtime(self.timestamp)
        return f"{self.participant.registration_id} at {local_time}"
