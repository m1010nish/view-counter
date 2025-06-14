from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os

# --- Flask setup ---
app = Flask(__name__)
CORS(app)

# --- Database config ---
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:QkeGuwmSRraAfWrYUJSBTBprqmhGwHSC@postgres.railway.internal:5432/railway")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- DB model ---
class View(Base):
    __tablename__ = "views"
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- Create tables ---
Base.metadata.create_all(engine)

@app.route("/increment-view", methods=["GET"])
def increment_view():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    session = SessionLocal()

    existing_view = session.query(View).filter_by(ip_address=ip).first()

    if not existing_view:
        new_view = View(ip_address=ip)
        session.add(new_view)
        session.commit()
        unique = True
    else:
        unique = False

    total_views = session.query(View).count()
    session.close()

    return jsonify({
        "views": total_views,
        "your_ip": ip,
        "unique": unique
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
