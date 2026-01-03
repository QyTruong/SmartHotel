echo "=== Cài đặt thư viện ==="
pip install -r requirements.txt

echo "=== Tạo superuser ==="
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=truong.4725212@gmail.com
export DJANGO_SUPERUSER_PASSWORD=admin123456

python manage.py createsuperuser --no-input || echo "SuperUser đã tồn tại!"

echo "=== Khởi tạo dữ liệu mẫu ==="
python manage.py shell  <<EOF
from smarthotel.models import Category
c1, _ = Category.objects.get_or_create(name='vip')
c2, _ = Category.objects.get_or_create(name='standard')

EOF
