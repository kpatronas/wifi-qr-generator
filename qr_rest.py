from flask import Flask, jsonify, request, send_file
from PIL import ImageFont, ImageDraw, Image
from flask_restful import Api, Resource
import qrcode
import io

app = Flask(__name__)
api = Api(app)

class WifiQRGenerator(Resource):
    def post(self):
        data = request.get_json()
        ssid        = data.get('ssid')
        password    = data.get('password')
        description = data.get('description')

        if not ssid or not password:
            return jsonify({"error": "SSID and password are required!"}), 400

        wifi_str = f"WIFI:T:WPA;S:{ssid};P:{password};;"

        # Create QR code
        qr = qrcode.QRCode(
            version          = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size         = 10,
            border           = 4,
        )

        qr.add_data(wifi_str)
        qr.make(fit = True)

        # Generate image
        img = qr.make_image(fill       = 'black',
                            back_color = 'white').convert('RGBA')

        # Add Description
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Get the size of the QR code and description text
        img_width, img_height = img.size
        bbox = draw.textbbox((0, 0), description, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        #text_width, text_height = draw.textsize(description, font=font)

        # Create a new image with extra space for the description
        new_img = Image.new('RGBA', (img_width, img_height + text_height + 10), 'white')
        new_img.paste(img, (0, 0))

        # Draw the description text onto the new image
        text_position = ((new_img.size[0] - text_width) // 2, img_height + 5)  # Center text
        draw = ImageDraw.Draw(new_img)
        draw.text(text_position, description, font=font, fill='black')

        # Save to byte array as before
        img_byte_arr = io.BytesIO()
        new_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Send the image file as response
        filename = f"{description.replace(' ', '_')}_wifi_qr_code.png" if description else 'wifi_qr_code.png'
        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name=filename)


# Add resource to API
api.add_resource(WifiQRGenerator, '/generate_qr')

if __name__ == '__main__':
    app.run(debug=True)
