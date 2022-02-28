from PIL import Image
import os

new_width = 50

for f in os.listdir():
	if f.endswith('.png'):
		i = Image.open(f)

		f_name, f_ext = os.path.splitext(f)

		old_width = i.size[0]
		old_heigth = i.size[1]

		new_heigth = int((new_width * old_heigth / old_width))

		i.thumbnail((new_width, new_heigth))
		# save new resize picture to "pic_assets" folder
		i.save(f'Assets/{f_name}{f_ext}')
