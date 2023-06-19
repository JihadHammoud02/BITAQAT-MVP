from .models import QrCodeChecking as NFTMetadata


query=NFTMetadata.objects.all()

for obj in query:
    obj.delete()

