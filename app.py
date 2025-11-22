import threading
from flask import Flask, render_template, jsonify
from bot_core import BotService

app = Flask(__name__)

API_TOKEN = 'TOKENINIZI_BURAYA_YAPISTIRIN' 

bot_service = BotService(API_TOKEN)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    return jsonify({'running': bot_service.is_running})

@app.route('/api/start', methods=['POST'])
def start_bot():
    if not bot_service.is_running:
        t = threading.Thread(target=bot_service.start)
        t.daemon = True
        t.start()
        return jsonify({'status': 'success', 'message': 'Bot servisi başlatıldı.'})
    return jsonify({'status': 'warning', 'message': 'Bot zaten çalışıyor.'})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    if bot_service.is_running:
        bot_service.stop()
        return jsonify({'status': 'success', 'message': 'Bot servisi durduruldu.'})
    return jsonify({'status': 'warning', 'message': 'Bot zaten kapalı.'})

if __name__ == '__main__':
    app.run(debug=False, port=5000)