import io
import base64
import secrets
import qrcode
from qrcode.constants import ERROR_CORRECT_M

# 31 unambiguous uppercase alphanumeric characters (no 0/O, no 1/I/L)
KEY_CHARSET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_share_key() -> str:
    """
    Generates a cryptographically random 8-character Share Key formatted as XXXX-XXXX.
    Uses secrets.choice from an unambiguous alphanumeric character set.
    """
    first_half = "".join(secrets.choice(KEY_CHARSET) for _ in range(4))
    second_half = "".join(secrets.choice(KEY_CHARSET) for _ in range(4))
    return f"{first_half}-{second_half}"


def generate_qr_image_buffer(url: str) -> io.BytesIO:
    """
    Generates a high-contrast QR code image for a target URL and returns it as a BytesIO PNG buffer.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate styled high-contrast QR image
    img = qr.make_image(fill_color="#090d16", back_color="#ffffff")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_qr_data_uri(url: str) -> str:
    """
    Generates a QR code and returns an inline Base64 data URI string for seamless template embedding.
    """
    buffer = generate_qr_image_buffer(url)
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_data}"
