from .models import NFTMetadata


query=NFTMetadata.objects.all()

for obj in query:
    obj.delete()

