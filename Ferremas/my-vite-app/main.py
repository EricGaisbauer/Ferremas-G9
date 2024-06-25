from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Habilitar CORS para todas las rutas
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Despacho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(70), unique=True)
    proceso = db.Column(db.String(100))
    
    def __init__(self, producto, proceso):
        self.producto = producto
        self.proceso = proceso

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'producto', 'proceso')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/task', methods=['POST'])
def create_task():
    if request.is_json:
        data = request.json
        new_task = Despacho(producto=data.get('producto'), proceso=data.get('proceso'))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Tarea creada exitosamente'}), 201
    else:
        return jsonify({'message': 'La solicitud debe ser JSON'}), 400

@app.route('/task', methods=['GET'])
def get_tasks():
    all_tasks = Despacho.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
