Run Links: Frontend `http://127.0.0.1:5173/` | Backend Health `http://127.0.0.1:8000/health`

# Smart Assignment Maker

Smart Assignment Maker turns typed assignment or practical text into a print-ready handwritten PDF.

## Features

- Handwritten PDF generation with blue, black, and pencil ink.
- Ruled, blank, graph grid, and ABES practical sheet paper styles.
- Student metadata fields for name, roll number, college, subject, and date.
- Adjustable font size, line gap, left margin, top margin, header position, handwriting shake, smudge, scan noise, and shadows.
- Ten handwriting font profiles. Missing profiles auto-heal from the backend when network access is available.
- Frontend API status badge and backend `/health` route for deploy checks.

## Local Run

Backend:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env` from `frontend/.env.example` when the API is not running on `http://127.0.0.1:8000`.

## Deploy Notes

- Deploy the backend from the repository root with `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
- Deploy the frontend from the `frontend` folder.
- Set `VITE_API_URL` on the frontend host to the deployed backend URL.
- The nested `smart-practical-maker/frontend` folder is kept in sync as a fallback copy, but the primary frontend is `frontend`.
