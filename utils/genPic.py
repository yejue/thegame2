import random
from PIL import Image
from io import BytesIO


def gen_rancolor():
    tags = [chr(i) for i in range(97, 104)]
    tags.extend([str(i) for i in range(10)])
    return '#' + ''.join([random.choice(tags) for _ in range(6)])


def gen_pure(width=133, height=56, string=None):
    try:
        new = Image.new("RGB", (width, height), gen_rancolor())
        out = BytesIO()
        fmt = "png"
        new.save(out, format(fmt))
        return out.getvalue() + ("<恭喜你找到了验证码:{}>".format(string)).encode()
    except ValueError:
        gen_pure(width, height, string)


if __name__ == '__main__':
    gen_pure(130, 130)
