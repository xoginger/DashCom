# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import db, Report, Meta, User
import threading

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    # Inicializar metas por defecto si no existen
    if not Meta.query.filter_by(name='respuestas_semanal').first():
        db.session.add(Meta(name='respuestas_semanal', value=5))
    if not Meta.query.filter_by(name='respuestas_mensual').first():
        db.session.add(Meta(name='respuestas_mensual', value=20))
    db.session.commit()

@app.route("/")
def dashboard():
    reports = Report.query.order_by(Report.timestamp.desc()).limit(20).all()
    meta_semanal = Meta.query.filter_by(name='respuestas_semanal').first()
    meta_mensual = Meta.query.filter_by(name='respuestas_mensual').first()
    return render_template("dashboard.html", reports=reports, meta_semanal=meta_semanal, meta_mensual=meta_mensual)

@app.route("/api/reports")
def api_reports():
    reports = Report.query.order_by(Report.timestamp.desc()).limit(20).all()
    data = [{
        "user": r.user.name if r.user else "Desconocido",
        "timestamp": r.timestamp.isoformat(),
        "content": r.content
    } for r in reports]
    return jsonify(data)

@app.route("/admin/metas", methods=["GET", "POST"])
def admin_metas():
    if request.method == "POST":
        respuestas_semanal = request.form.get("respuestas_semanal")
        respuestas_mensual = request.form.get("respuestas_mensual")
        
        meta_semanal = Meta.query.filter_by(name='respuestas_semanal').first()
        meta_mensual = Meta.query.filter_by(name='respuestas_mensual').first()
        
        if meta_semanal and meta_mensual:
            meta_semanal.value = int(respuestas_semanal)
            meta_mensual.value = int(respuestas_mensual)
            db.session.commit()
            flash("Metas actualizadas correctamente.", "success")
        return redirect(url_for("admin_metas"))
    else:
        meta_semanal = Meta.query.filter_by(name='respuestas_semanal').first()
        meta_mensual = Meta.query.filter_by(name='respuestas_mensual').first()
        return render_template("admin_metas.html", meta_semanal=meta_semanal, meta_mensual=meta_mensual)

def run_telegram_bot():
    from telegram_bot import setup_bot
    from config import Config
    bot_app = setup_bot(Config)
    bot_app.run_polling()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    app.run(port=5000, debug=True)
