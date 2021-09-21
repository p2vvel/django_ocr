from PIL import Image

filenames = ['a.png', 'b.jpg', 'c.jpg', 'd.png', 'e.png']

# for k in filenames:
#     temp = Image.open(k)
#     new_temp = temp.rotate(180, expand=True)
#     new_temp.save("rotated_180_"+temp.filename)

for k in filenames:
    temp = Image.open(k)
    new_temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    new_temp.save("mirror_x_"+temp.filename)

for k in filenames:
    temp = Image.open(k)
    new_temp = temp.transpose(Image.FLIP_TOP_BOTTOM)
    new_temp.save("mirror_y_"+temp.filename)