
from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/etiqueta', methods=['POST'])
def etiqueta():
    remetente = request.form['remetente']
    destinatario = request.form['destinatario']
    transportadora = request.form['transportadora']
    mercadoria = request.form['mercadoria']

    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # Define dimensões da etiqueta 10x15 (mm)
    largura = 100
    altura = 150
    x = 10
    y = 10

    for i in range(2):  # duas etiquetas por folha
        pdf.set_xy(x, y + (i * (altura + 10)))
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(largura, 10, "REMETENTE", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(largura, 7, remetente)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(largura, 10, "DESTINATÁRIO", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(largura, 7, destinatario)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(largura, 10, f"TRANSPORTADORA: {transportadora}", ln=True)
        pdf.cell(largura, 10, f"MERCADORIA: {mercadoria} 📦", ln=True)

    # Salvar em memória
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="etiqueta.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
