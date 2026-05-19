import os
import cloudinary.uploader
from django.core.files.storage import Storage


class CloudinaryStorage(Storage):
    """Storage backend minimal utilisant directement l'API cloudinary."""

    def _save(self, name, content):
        public_id = os.path.splitext(name)[0]
        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
            resource_type='auto',
        )
        return result['secure_url']

    def url(self, name):
        return name or ''

    def exists(self, name):
        return False

    def delete(self, name):
        pass
