from PIL import Image

# Membuat gambar latar belakang baru
background = Image.new('RGBA', (1000, 1000), (255, 255, 255, 0))
overlay = Image.open('111.png').convert('RGBA')

# Meminta pengguna untuk memasukkan lebar gambar
overlay_width = int(input("Masukkan lebar gambar: "))
overlay = overlay.resize((overlay_width, overlay_width))

# Meminta pengguna untuk memasukkan koordinat X dan Y
x = int(input("Masukkan koordinat X: ".format(1000 - overlay_width)))
y = int(input("Masukkan koordinat Y: ".format(1000 - overlay_width)))

# Memastikan koordinat berada dalam rentang yang diperbolehkan
if 0 <= x <= (1000 - overlay_width) and 0 <= y <= (1000 - overlay_width):
    background.paste(overlay, (x, y), overlay.split()[3])
    background.save('orig4.png', format='PNG')
    print(f'\nGambar berhasil dibuat\n\nKoordinat ({x}, {x + overlay_width-1}, {y}, {y + overlay_width-1})')
else:
    print("Koordinat berada di luar rentang yang diperbolehkan.")

