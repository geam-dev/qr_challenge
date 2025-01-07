import qrcode, io 

def get_qr_code_img_bytes(
    data: str,
    size: str,
    color: str,
):
    bytes_image = io.BytesIO()

    qr = qrcode.QRCode(
        version=1,
        box_size=size,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color="white")
    img.save(bytes_image, format="PNG")

    return bytes_image.getvalue()