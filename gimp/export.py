import math
image = gimp.image_list()[0]
for i in range(2):
    if i == 1:
        pdb.gimp_image_scale(image, math.ceil(image.width / 2), math.ceil(image.height / 2))
    # set everything as disabled
    for layer in image.layers:
        layer.visible = False
    for group in image.layers:
        if not group.layers:
            continue
        group.visible = True
        for layer in group.layers:
            layer.visible = True
            # set all other layers disabled
            for l in group.layers:
                if l == layer:
                    continue
                # grey color tag marks bg
                if pdb.gimp_item_get_color_tag(l) == 8:
                    continue
                l.visible = False
            # export
            pdb.gimp_file_save(image, group, f"{group.name}-{layer.name}.jpg", "?")
        group.visible = False