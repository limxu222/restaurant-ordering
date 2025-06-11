import qrcode
url = "http://localhost:5000"  # or your deployed URL
img = qrcode.make(url)
img.save("restaurant_qr.png")
print("QR code saved")
