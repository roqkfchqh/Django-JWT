#!/usr/bin/env bash

# ------- 설정 값 --------
AWS_REGION="ap-northeast-2"
UBUNTU_AMI_ID="ami-0d5bb3742db8fc264"
INSTANCE_TYPE="t2.micro"
KEY_NAME="roqkf"
SECURITY_GROUP_NAME="lcy-ec2-sg-py"
SECURITY_GROUP_DESC="Allow 8000 for Django App"
REPO_URL="https://github.com/roqkfchqh/Django-JWT.git"
APP_DIR="/home/ubuntu/app"
PORT=8000
TAG="Homework"
GRADLE_VERSION="8.5"
# ------- 설정 값 --------

# 1) 보안 그룹 생성 & 8000, SSH 허용
SG_EXISTS=$(aws ec2 describe-security-groups \
  --group-names "$SECURITY_GROUP_NAME" \
  --region "$AWS_REGION" 2>/dev/null | jq -r '.SecurityGroups[0].GroupId' || true)

if [ -z "$SG_EXISTS" ]; then
  aws ec2 create-security-group \
    --group-name "$SECURITY_GROUP_NAME" \
    --description "$SECURITY_GROUP_DESC" \
    --region "$AWS_REGION" >/dev/null
else
  echo "보안 그룹 '$SECURITY_GROUP_NAME'이 이미 존재합니다."
fi

aws ec2 authorize-security-group-ingress \
  --group-name "$SECURITY_GROUP_NAME" \
  --protocol tcp \
  --port "$PORT" \
  --cidr 0.0.0.0/0 \
  --region "$AWS_REGION" >/dev/null 2>/dev/null || true

aws ec2 authorize-security-group-ingress \
  --group-name "$SECURITY_GROUP_NAME" \
  --protocol tcp \
  --port 22 \
  --cidr 211.224.58.200/32 \
  --region "$AWS_REGION" >/dev/null 2>/dev/null || true

# 2) user‑data 스크립트 작성
read -r -d '' USER_DATA <<EOF
#!/bin/bash
set -e

# --- 로그 설정 ---
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo "User Data 스크립트 시작: \$(date)"

# --- 시스템 업데이트 ---
apt-get update -y
apt-get upgrade -y

# --- Python 및 pip 설치 ---
apt-get install -y python3 python3-pip python3-venv git

# --- 앱 디렉토리 준비 ---
APP_DIR="/home/ubuntu/app"
REPO_URL="${REPO_URL}"
PORT=8000
mkdir -p \$APP_DIR
chown ubuntu:ubuntu \$APP_DIR

# --- Django 프로젝트 클론 및 설정 ---
sudo -u ubuntu bash -lc "
  git clone \$REPO_URL \$APP_DIR &&
  cd \$APP_DIR &&
  python3 -m venv venv &&
  source venv/bin/activate &&
  pip install --upgrade pip &&
  pip install -r requirements.txt
"

# --- 백그라운드 실행 ---
sudo -u ubuntu bash -lc "
  cd \$APP_DIR &&
  source venv/bin/activate
  cd django-jwt
  python manage.py runserver 0.0.0.0:\$PORT
"
EOF

# 3) EC2 인스턴스 생성
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$UBUNTU_AMI_ID" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-groups "$SECURITY_GROUP_NAME" \
  --user-data "$USER_DATA" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$TAG}]" \
  --query 'Instances[0].InstanceId' \
  --output text \
  --region "$AWS_REGION")

echo "인스턴스 생성 중 ($INSTANCE_ID)"

# 4) running 대기
aws ec2 wait instance-running \
  --instance-ids "$INSTANCE_ID" \
  --region "$AWS_REGION"

# 5) 퍼블릭 DNS 확인
PUBLIC_DNS=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicDnsName' \
  --output text \
  --region "$AWS_REGION")

if [ -z "$PUBLIC_DNS" ] || [ "$PUBLIC_DNS" == "None" ]; then
  PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text \
    --region "$AWS_REGION")
  echo "EC2($INSTANCE_ID) 준비 완료 http://$PUBLIC_IP:$PORT"
else
  echo "EC2($INSTANCE_ID) 준비 완료 http://$PUBLIC_DNS:$PORT"
fi
