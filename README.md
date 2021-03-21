Python SQLite Class Generator
==============
Class generator written in python

# Example

```Python
from generator.modelobjectgenerator import ModelobjectGenerator
generator = ModelobjectGenerator("/opt/app/tmp/Contact.sqlite")
output = "/opt/app/tmp/"
generator.generate_classes(output)
```

## Result Example
```Python
class Phone:
	persistent="Phone"
	def __init__(self , pid, number, contact_id):
		self.pid=pid
		self.number=number
		self.whatsapp=0
		self.contact_id=contact_id

```
#License

MIT License (MIT)
