import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 보안키: Render 환경변수 SECRET_KEY 사용 (없으면 로컬용 기본값)
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me")

# DEBUG: 로컬은 True로 쓰고 싶으면 환경변수 DEBUG=True로 설정
DEBUG = os.environ.get("DEBUG", "False") == "True"

# 데모/과제용으로 일단 전체 허용 (원하면 Render 도메인만 넣어도 됨)
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # ✅ Render에서 Django(Gunicorn)로 정적파일 서빙하려면 Whitenoise 필수
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "grade_mgmt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # templates/ 사용
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "grade_mgmt.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# =========================
# ✅ Static files (중요!!)
# =========================
STATIC_URL = "/static/"

# ✅ 너는 CSS가 "프로젝트 루트/static/" 아래에 있으므로 반드시 필요
#    (A) static/core/style.css 를 collectstatic 대상에 포함시킴
STATICFILES_DIRS = [BASE_DIR / "static"]

# ✅ collectstatic 결과가 모이는 폴더 (배포에서 이걸 Whitenoise가 서빙)
STATIC_ROOT = BASE_DIR / "staticfiles"

# ✅ Whitenoise 권장 설정 (캐시/압축/해시 처리)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
