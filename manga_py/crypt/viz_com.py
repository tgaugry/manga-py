import re
from typing import List, Optional, Tuple
from PIL import Image
from pathlib import Path


class VizComMatrix:
    @classmethod
    def get_image_meta(cls, path: str) -> Optional[List[int]]:
        pattern = None
        try:
            with open(path, 'rb') as r:
                # read one line. get pattern
                pattern = re.search(r'([\da-f]{2}(?::[\da-f]{2})+)', str(r.readline())).group(1)
                pattern = [int('0x%s' % i, 16) for i in pattern.split(':')]
        except Exception as e:
            print('Error extract pattern. Path: %s' % path)
        return pattern

    @classmethod
    def solve_image(cls, path: str) -> Optional[Image.Image]:
        meta = cls.get_image_meta(path)
        if meta is None:
            return

        orig = Image.open(path)  # type: Image.Image
        ref = Image.new(orig.mode, orig.size)  # type: Image.Image
        ref.paste(orig)

        width, height = orig.size
        new_width = int(width / 10)
        new_height = int(height / 15)

        ref = cls.paste(ref, orig, (
            0, int(new_height + 10),
            int(new_width), int(height - 2 * new_height),
        ), (
            0, int(new_height),
            int(new_width), int(height - 2 * new_height),
        ))

        ref = cls.paste(ref, orig, (
            0, int(14 * (new_height + 10)),
            width, int(height - 14 * (new_height + 0)),
        ), (
            0, int(14 * new_height),
            width, int(height - 14 * (new_height + 0)),
        ))

        ref = cls.paste(ref, orig, (
            int(9 * (new_width + 10)), int(new_height + 10),
            int(new_width + (width - 10 * new_width)), int(height - 2 * new_height),
        ), (
            int(9 * new_width), int(new_height),
            int(new_width + (width - 10 * new_width)), int(height - 2 * new_height),
        ))

        for i, size in enumerate(meta):
            ref = cls.paste(ref, orig, (
              int((i % 8 + 1) * (new_width + 10)), int((float(i / 8) + 1) * (new_height + 10)),
              int(new_width), int(new_height),
            ), (
                int((size % 8 + 1) * new_width), int((float(size / 8) + 1) * new_height),
                int(new_width), int(new_height),
            ))

        return ref

    @classmethod
    def paste(cls, ref: Image.Image, orig: Image.Image, orig_box: Tuple, ref_box: Tuple) -> Image.Image:

        ref.paste(orig.crop((
            orig_box[0], orig_box[1],
            orig_box[0] + orig_box[2], orig_box[1] + orig_box[3],
        )), (
            ref_box[0], ref_box[1],
            ref_box[0] + ref_box[2], ref_box[1] + ref_box[3],
        ))

        return ref

    # see '.readerImgPage'
    #
    # preloadImages()
    # pageKeys[]
    #
    # line 3800:
    # /** @type {number} */
    # const width = parseInt(pageKeys["page" + context].width);
    # /** @type {number} */
    # const height = parseInt(pageKeys["page" + context].height);
    # /** @type {number} */
    # var new_w = Math.floor(width / 10);
    # /** @type {number} */
    # var new_h = Math.floor(height / 15);
    # var IEVersion = name.split(":");
    # ctx.drawImage(g_avatarImage,
    #     0, 0,
    #     width, new_h,
    #
    #     0, 0,
    #     width, new_h
    # );
    # ctx.drawImage(g_avatarImage,
    #     0, new_h + 10,
    #     new_w, height - 2 * new_h,
    #
    #     0, new_h, new_w,
    #     height - 2 * new_h
    # );
    # ctx.drawImage(g_avatarImage,
    #     0, 14 * (new_h + 10),
    #     width, g_avatarImage.height - 14 * (new_h + 10),
    #
    #     0, 14 * new_h,
    #     width, g_avatarImage.height - 14 * (new_h + 10)
    # );
    # ctx.drawImage(g_avatarImage,
    #     9 * (new_w + 10), new_h + 10,
    #     new_w + (width - 10 * new_w), height - 2 * new_h,
    #
    #     9 * new_w, new_h,
    #     new_w + (width - 10 * new_w), height - 2 * new_h
    # );
    # /** @type {number} */
    # i = 0;
    # for (; i < IEVersion.length; i++) {
    #   /** @type {number} */
    #   IEVersion[i] = parseInt(IEVersion[i], 16);
    #   ctx.drawImage(
    #       g_avatarImage,
    #       Math.floor((i % 8 + 1) * (new_w + 10)), Math.floor((Math.floor(i / 8) + 1) * (new_h + 10)),
    #       Math.floor(new_w), Math.floor(new_h),
    #
    #       Math.floor((IEVersion[i] % 8 + 1) * new_w), Math.floor((Math.floor(IEVersion[i] / 8) + 1) * new_h),
    #       Math.floor(new_w), Math.floor(new_h)
    #   );
    # }


solve = VizComMatrix().solve_image

__all__ = ['solve']