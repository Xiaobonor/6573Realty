from flask import Blueprint, send_file, abort, render_template
import base64
import io
from app.models.rental_property import RentalProperty

image_viewer_bp = Blueprint('image_viewer_bp', __name__)


@image_viewer_bp.route('/test/<uuid>')
def test(uuid):
    rental_property = RentalProperty.get_property_by_uuid(uuid)
    return render_template('email/match_with_user.html', property=rental_property)

@image_viewer_bp.route('/view/<uuid>/<int:page>')
def serve_image(uuid, page):
    rental_property = RentalProperty.get_property_by_uuid(uuid)
    if not rental_property:
        abort(404, description="Property not found")

    if page < 1 or page > len(rental_property.images):
        abort(404, description="Image not found")

    base64_image = rental_property.images[page - 1]
    print(base64_image)
    print(len(base64_image))

    if base64_image.startswith('data:image/png;base64,'):
        base64_image_cleaned = base64_image[len('data:image/png;base64,'):]
        mimetype = 'image/png'
    elif base64_image.startswith('data:image/jpeg;base64,') or base64_image.startswith('data:image/jpg;base64,'):
        base64_image_cleaned = base64_image.split('base64,')[1]
        mimetype = 'image/jpeg'
    elif base64_image.startswith('data:image/webp;base64,'):
        base64_image_cleaned = base64_image[len('data:image/webp;base64,'):]
        mimetype = 'image/webp'
    elif base64_image.startswith('data:image/gif;base64,'):
        base64_image_cleaned = base64_image[len('data:image/gif;base64,'):]
        mimetype = 'image/gif'
    else:
        abort(400, description="Unsupported image type")

    missing_padding = len(base64_image_cleaned) % 4
    if missing_padding:
        print("Missing padding")
        base64_image_cleaned += '=' * (4 - missing_padding)

    image_data = base64.b64decode(base64_image_cleaned)
    image_io = io.BytesIO(image_data)
    return send_file(image_io, mimetype=mimetype, as_attachment=False, download_name='image.png')