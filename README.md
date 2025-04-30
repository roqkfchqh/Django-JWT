# 🟧 Django + JWT 백엔드 템플릿

---

## 🟧 목차
0. [테스트코드 실행법](#테스트코드-실행법)
1. [파일 구조](#파일-구조)
2. [기술 스택](#기술-스택)
3. [API](#api)
4. [JWT](#JWT)
5. [EC2 자동 배포 스크립트](#ec2-자동-배포-스크립트-deploysh)
6. [Swagger 연동](#swagger-연동)

___

## 🟧 테스트코드 실행법

1. 프로젝트 클론
```bash
git clone <repo-url>
cd Django-JWT
```

2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 테스트 코드 실행
```bash
cd django-jwt
pytest
```

---
## 🟧 파일 구조

```markdown
django-jwt/
├── auth_app/
│   ├── jwt_utils.py         # JWT 생성/검증 유틸
│   ├── schemas.py           # Swagger 문서용 serializer 및 예시
│   ├── test_auth.py         # 인증 관련 테스트 코드
│   ├── urls.py              # 인증 API 라우터
│   ├── user_store.py        # 인메모리 사용자 저장소
│   └── views.py             # 회원가입/로그인 등 API 구현

├── jwt_project/
│   ├── settings.py          # Django 설정 파일 (DRF, JWT 설정 포함)
│   └── urls.py              # 전체 URL 라우팅 (auth_app 연결)

├── manage.py                # Django 실행 스크립트
├── requirements.txt         # 의존성 패키지 목록
├── deploy.sh                # EC2 자동 배포 스크립트
└── pytest.ini               # 테스트 설정

```

---

## 🟧 기술 스택
| 분야 | 내용                           |
|-----|------------------------------|
| 언어 | Python 3.13                 |
| 프레임워크 | 	Django 4.x              |
| 인증/인가 | PyJWT         |
| 문서화 | Swagger (spectacular)  |
| 배포 | AWS EC2 + Bash 스크립트          |
| 가상환경 | venv                        |

---

## 🟧 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /register | 사용자 회원가입 |
| POST | /login | 로그인 후 JWT 토큰 발급 |
| GET | /me | 내 정보 조회(인증 필요) |

---
## 🟧 JWT

- PyJWT 기반으로 가볍고 빠름, 외부 의존 최소화
- DB 없이 메모리 기반 유저 인증 구조

---


## 🟧 EC2 자동 배포 스크립트 (deploy.sh)

### 주요 흐름
1. 보안 그룹 생성 및 포트(8000, 22) 오픈
2. EC2 인스턴스 생성 (Python, pip, venv 설치 포함)
3. GitHub에서 Django 프로젝트 클론
4. 가상환경 설정 및 requirements.txt 설치
5. manage.py runserver 백그라운드 실행
> ec2 내부에서 settings.py 수정 필요

### 실행 결과 예시
```
EC2(i-xxxxxxxx) 준비 완료 http://ec2-xx-xxx-xxx-xxx.compute.amazonaws.com:8000
```

---

## 🟧 Swagger 연동
- drf-spectacular 사용
- 각 API에 @swagger_auto_schema, @extend_schema 등 명시
- Authorization 헤더 입력 가능 (Bearer token)
- 에러 응답도 schema로 자동 문서화됨

---

