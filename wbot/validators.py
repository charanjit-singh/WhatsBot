from django.core.exceptions import ValidationError
import magic


class MimetypeValidator(object):
	def __init__(self, mimetypes):
		self.mimetypes = mimetypes

	def __call__(self, value):
		try:
			mime = magic.from_buffer(value.read(1024), mime=True)
			print(mime)
			if not mime in self.mimetypes:
				raise ValidationError('%s is not an acceptable file type' % value)
		except AttributeError as e:
			raise ValidationError('This value could not be validated for file type' % value)
