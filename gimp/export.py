import math, os
out = "out"
image = pdb.gimp_image_duplicate(gimp.image_list()[0])
if not os.path.isdir(out):
    os.mkdir(out)
# set everything as disabled
for layer in image.layers:
    if pdb.gimp_item_get_color_tag(layer) == 8: # bg, always on
        continue
    layer.visible = False

# export each group
for group in image.layers:
    if not hasattr(group, "layers"):
        continue
    group.visible = True
    for layer in group.layers:
        if pdb.gimp_item_get_color_tag(layer) == 8: # bg
            continue
        layer.visible = True
        # set all other layers disabled
        for l in group.layers:
            if l == layer:
                continue
            # grey color tag marks bg, always on
            if pdb.gimp_item_get_color_tag(l) == 8:
                continue
            l.visible = False
        # export
        dir = out + "/" + group.name.lower()
        base = dir + "/" + layer.name.lower()
        if not os.path.isdir(dir):
            os.mkdir(dir)
        # duplicate and merge
        dupe = pdb.gimp_image_duplicate(image)
        content = pdb.gimp_image_merge_visible_layers(dupe, CLIP_TO_IMAGE)
        pdb.gimp_file_save(dupe, content, base + ".jpg", "?")
        # half scale
        pdb.gimp_image_scale(dupe, math.ceil(dupe.width / 2), math.ceil(dupe.height / 2))
        pdb.gimp_file_save(dupe, content, base + "-small.jpg", "?")
        #delete dupe
        pdb.gimp_image_delete(dupe)
    group.visible = False

# enable everything again
for layer in image.layers:
    layer.visible = True


