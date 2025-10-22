# 🚀 AI Tax Advisor

## ขั้นตอนการรัน

### 1. เปิด Qdrant (Database)
```bash
docker-compose up -d
```

เช็คที่: http://localhost:6333/dashboard

### 2. รัน Backend

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# ⚠️ แก้ไข .env ใส่ OPENAI_API_KEY ก่อน!

python scripts/ingest_data.py
uvicorn app.main:app --reload
```

**Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ⚠️ แก้ไข .env ใส่ OPENAI_API_KEY ก่อน!

python scripts/ingest_data.py
uvicorn app.main:app --reload
```

เช็คที่: http://localhost:8000/docs

### 3. รัน Frontend (Terminal ใหม่)
```bash
cd frontend
npm install
npm run dev
```

เปิดเบราว์เซอร์: http://localhost:3000

## ⚠️ สิ่งที่ต้องทำเพิ่มเติม

1. **ดาวน์โหลดไฟล์โค้ดจาก Claude Artifacts:**
   - ไฟล์ Backend Python (11 ไฟล์)
   - ไฟล์ Frontend TypeScript (2 ไฟล์หลัก)

2. **แก้ไข backend/.env** ใส่ OpenAI API Key ของคุณ

3. **ดูรายละเอียดไฟล์ที่ต้องเพิ่ม** ใน Artifacts ทางด้านขวา
