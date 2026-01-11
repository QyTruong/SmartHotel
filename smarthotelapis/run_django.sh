echo "=== Tạo superuser ==="
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=truong.4725212@gmail.com
export DJANGO_SUPERUSER_PASSWORD=admin123456

python manage.py createsuperuser --no-input || echo "SuperUser đã tồn tại!"

echo "=== Khởi tạo dữ liệu mẫu ==="
python manage.py shell  <<EOF
from smarthotel.models import RoomCategory
c1, _ = RoomCategory.objects.get_or_create(name='Mot giuong', price=1500000)
c2, _ = RoomCategory.objects.get_or_create(name='Hai giuong', price=2000000)

EOF
